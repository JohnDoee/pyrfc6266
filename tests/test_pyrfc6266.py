import pytest
import requests

import pyrfc6266
from pyrfc6266 import ContentDisposition

# Tests sourced from http://test.greenbytes.de/tech/tc2231/


def test_greenbytes_inlonly():
    assert pyrfc6266.parse("inline") == ("inline", [])


def test_greenbytes_inlonlyquoted():
    with pytest.raises(pyrfc6266.ParseException):
        pyrfc6266.parse('"inline"')


def test_greenbytes_inlwithasciifilename():
    s = 'inline; filename="foo.html"'
    assert pyrfc6266.parse(s) == (
        "inline",
        [
            ContentDisposition("filename", "foo.html"),
        ],
    )
    assert pyrfc6266.parse_filename(s) == "foo.html"


def test_greenbytes_inlwithfnattach():
    assert pyrfc6266.parse('inline; filename="Not an attachment!"') == (
        "inline",
        [
            ContentDisposition("filename", "Not an attachment!"),
        ],
    )


def test_greenbytes_inlwithasciifilenamepdf():
    assert pyrfc6266.parse('inline; filename="foo.pdf"') == (
        "inline",
        [
            ContentDisposition("filename", "foo.pdf"),
        ],
    )


def test_greenbytes_attonly():
    assert pyrfc6266.parse("attachment") == ("attachment", [])


def test_greenbytes_attonlyquoted():
    with pytest.raises(pyrfc6266.ParseException):
        pyrfc6266.parse('"attachment"')


def test_greenbytes_attonlyucase():
    assert pyrfc6266.parse("ATTACHMENT") == ("attachment", [])


def test_greenbytes_attwithasciifilename():
    s = 'attachment; filename="foo.html"'
    assert pyrfc6266.parse(s) == (
        "attachment",
        [
            ContentDisposition("filename", "foo.html"),
        ],
    )
    assert pyrfc6266.parse_filename(s) == "foo.html"


def test_greenbytes_attwithasciifilename25():
    s = 'attachment; filename="0000000000111111111122222"'
    assert pyrfc6266.parse(s) == (
        "attachment",
        [
            ContentDisposition("filename", "0000000000111111111122222"),
        ],
    )
    assert pyrfc6266.parse_filename(s) == "0000000000111111111122222"


def test_greenbytes_attwithasciifilename35():
    s = 'attachment; filename="00000000001111111111222222222233333"'
    assert pyrfc6266.parse(s) == (
        "attachment",
        [
            ContentDisposition("filename", "00000000001111111111222222222233333"),
        ],
    )
    assert pyrfc6266.parse_filename(s) == "00000000001111111111222222222233333"


def test_greenbytes_attwithasciifnescapedchar():
    s = r'attachment; filename="f\oo.html"'
    assert pyrfc6266.parse(s) == (
        "attachment",
        [
            ContentDisposition("filename", "foo.html"),
        ],
    )
    assert pyrfc6266.parse_filename(s) == "foo.html"


def test_greenbytes_attwithasciifnescapedquote():
    s = r'attachment; filename="\"quoting\" tested.html"'
    assert pyrfc6266.parse(s) == (
        "attachment",
        [
            ContentDisposition("filename", '"quoting" tested.html'),
        ],
    )
    assert pyrfc6266.parse_filename(s) == '"quoting" tested.html'


def test_greenbytes_attwithquotedsemicolon():
    s = r'''attachment; filename="Here's a semicolon;.html"'''
    assert pyrfc6266.parse(s) == (
        "attachment",
        [
            ContentDisposition("filename", "Here's a semicolon;.html"),
        ],
    )
    assert pyrfc6266.parse_filename(s) == "Here's a semicolon;.html"


def test_greenbytes_attwithfilenameandextparam():
    s = r'''attachment; foo="bar"; filename="foo.html"'''
    assert pyrfc6266.parse(s) == (
        "attachment",
        [
            ContentDisposition("foo", "bar"),
            ContentDisposition("filename", "foo.html"),
        ],
    )
    assert pyrfc6266.parse_filename(s) == "foo.html"


def test_greenbytes_attwithfilenameandextparamescaped():
    s = r'''attachment; foo="\"\\";filename="foo.html"'''
    assert pyrfc6266.parse(s) == (
        "attachment",
        [
            ContentDisposition("foo", '"\\'),
            ContentDisposition("filename", "foo.html"),
        ],
    )
    assert pyrfc6266.parse_filename(s) == "foo.html"


def test_greenbytes_attwithasciifilenameucase():
    s = r'''attachment; FILENAME="foo.html"'''
    assert pyrfc6266.parse(s) == (
        "attachment",
        [
            ContentDisposition("filename", "foo.html"),
        ],
    )
    assert pyrfc6266.parse_filename(s) == "foo.html"


def test_greenbytes_attwithasciifilenamenq():
    s = r"""attachment; filename=foo.html"""
    assert pyrfc6266.parse(s) == (
        "attachment",
        [
            ContentDisposition("filename", "foo.html"),
        ],
    )
    assert pyrfc6266.parse_filename(s) == "foo.html"


def test_greenbytes_attwithtokfncommanq():
    with pytest.raises(pyrfc6266.ParseException):
        pyrfc6266.parse(r"""attachment; filename=foo,bar.html""")


def test_greenbytes_attwithasciifilenamenqs():
    with pytest.raises(pyrfc6266.ParseException):
        pyrfc6266.parse(r"""attachment; filename=foo.html ;""")


def test_greenbytes_attemptyparam():
    with pytest.raises(pyrfc6266.ParseException):
        pyrfc6266.parse(r"""attachment; ;filename=foo""")


def test_greenbytes_attwithasciifilenamenqws():
    with pytest.raises(pyrfc6266.ParseException):
        pyrfc6266.parse(r"""attachment; filename=foo bar.html""")


def test_greenbytes_attwithfntokensq():
    s = r"""attachment; filename='foo.bar'"""
    assert pyrfc6266.parse(s) == (
        "attachment",
        [
            ContentDisposition("filename", "'foo.bar'"),
        ],
    )
    assert pyrfc6266.parse_filename(s) == "'foo.bar'"


def test_greenbytes_attwithisofnplain():
    s = r'''attachment; filename="foo-ä.html"'''
    assert pyrfc6266.parse(s) == (
        "attachment",
        [
            ContentDisposition("filename", "foo-ä.html"),
        ],
    )
    assert pyrfc6266.parse_filename(s) == "foo-ä.html"


def test_greenbytes_attwithutf8fnplain():
    s = r'''attachment; filename="foo-Ã¤.html"'''
    assert pyrfc6266.parse(s) == (
        "attachment",
        [
            ContentDisposition("filename", "foo-Ã¤.html"),
        ],
    )
    assert pyrfc6266.parse_filename(s) == "foo-Ã¤.html"


def test_greenbytes_attwithfnrawpctenca():
    s = r'''attachment; filename="foo-%41.html"'''
    assert pyrfc6266.parse(s) == (
        "attachment",
        [
            ContentDisposition("filename", "foo-%41.html"),
        ],
    )
    assert pyrfc6266.parse_filename(s) == "foo-%41.html"


def test_greenbytes_attwithfnusingpct():
    s = r'''attachment; filename="50%.html"'''
    assert pyrfc6266.parse(s) == (
        "attachment",
        [
            ContentDisposition("filename", "50%.html"),
        ],
    )
    assert pyrfc6266.parse_filename(s) == "50%.html"


def test_greenbytes_attwithfnrawpctencaq():
    s = r'''attachment; filename="foo-%\41.html"'''
    assert pyrfc6266.parse(s) == (
        "attachment",
        [
            ContentDisposition("filename", "foo-%41.html"),
        ],
    )
    assert pyrfc6266.parse_filename(s) == "foo-%41.html"


def test_greenbytes_attwithnamepct():
    s = r'''attachment; name="foo-%41.html"'''
    assert pyrfc6266.parse(s) == (
        "attachment",
        [
            ContentDisposition("name", "foo-%41.html"),
        ],
    )


def test_greenbytes_attwithfilenamepctandiso():
    s = r'''attachment; filename="ä-%41.html"'''
    assert pyrfc6266.parse(s) == (
        "attachment",
        [
            ContentDisposition("filename", "ä-%41.html"),
        ],
    )
    assert pyrfc6266.parse_filename(s) == "ä-%41.html"


def test_greenbytes_attwithfnrawpctenclong():
    s = r'''attachment; filename="foo-%c3%a4-%e2%82%ac.html"'''
    assert pyrfc6266.parse(s) == (
        "attachment",
        [
            ContentDisposition("filename", "foo-%c3%a4-%e2%82%ac.html"),
        ],
    )
    assert pyrfc6266.parse_filename(s) == "foo-%c3%a4-%e2%82%ac.html"


def test_greenbytes_attwithasciifilenamews1():
    s = r'''attachment; filename ="foo.html"'''
    assert pyrfc6266.parse(s) == (
        "attachment",
        [
            ContentDisposition("filename", "foo.html"),
        ],
    )
    assert pyrfc6266.parse_filename(s) == "foo.html"


def test_greenbytes_attwith2filenames():
    with pytest.raises(pyrfc6266.ParseException):
        pyrfc6266.parse(r'''attachment; filename="foo.html"; filename="bar.html"''')


def test_greenbytes_attfnbrokentoken():
    with pytest.raises(pyrfc6266.ParseException):
        pyrfc6266.parse(r"""attachment; filename=foo[1](2).html""")


def test_greenbytes_attfnbrokentokeniso():
    with pytest.raises(pyrfc6266.ParseException):
        pyrfc6266.parse(r"""attachment; filename=foo-ä.html""")


def test_greenbytes_attfnbrokentokenutf():
    with pytest.raises(pyrfc6266.ParseException):
        pyrfc6266.parse(r"""attachment; filename=foo-Ã¤.html""")


def test_greenbytes_attmissingdisposition():
    with pytest.raises(pyrfc6266.ParseException):
        pyrfc6266.parse(r"""filename=foo.html""")


def test_greenbytes_attmissingdisposition2():
    with pytest.raises(pyrfc6266.ParseException):
        pyrfc6266.parse(r"""x=y; filename=foo.html""")


def test_greenbytes_attmissingdisposition3():
    with pytest.raises(pyrfc6266.ParseException):
        pyrfc6266.parse(r""""foo; filename=bar;baz"; filename=qux""")


def test_greenbytes_attmissingdisposition4():
    with pytest.raises(pyrfc6266.ParseException):
        pyrfc6266.parse(r"""filename=foo.html, filename=bar.html""")


def test_greenbytes_emptydisposition():
    with pytest.raises(pyrfc6266.ParseException):
        pyrfc6266.parse(r"""; filename=foo.html""")


def test_greenbytes_doublecolon():
    with pytest.raises(pyrfc6266.ParseException):
        pyrfc6266.parse(r""": inline; attachment; filename=foo.html""")


def test_greenbytes_attandinline():
    with pytest.raises(pyrfc6266.ParseException):
        pyrfc6266.parse(r"""inline; attachment; filename=foo.html""")


def test_greenbytes_attandinline2():
    with pytest.raises(pyrfc6266.ParseException):
        pyrfc6266.parse(r"""attachment; inline; filename=foo.html""")


def test_greenbytes_attbrokenquotedfn():
    with pytest.raises(pyrfc6266.ParseException):
        pyrfc6266.parse(r"""attachment; filename="foo.html".txt""")


def test_greenbytes_attbrokenquotedfn2():
    with pytest.raises(pyrfc6266.ParseException):
        pyrfc6266.parse(r"""attachment; filename="bar""")


def test_greenbytes_attbrokenquotedfn3():
    with pytest.raises(pyrfc6266.ParseException):
        pyrfc6266.parse(r"""attachment; filename=foo"bar;baz"qux""")


def test_greenbytes_attmultinstances():
    with pytest.raises(pyrfc6266.ParseException):
        pyrfc6266.parse(
            r"""attachment; filename=foo.html, attachment; filename=bar.html"""
        )


def test_greenbytes_attmissingdelim():
    with pytest.raises(pyrfc6266.ParseException):
        pyrfc6266.parse(r"""attachment; foo=foo filename=bar""")


def test_greenbytes_attmissingdelim2():
    with pytest.raises(pyrfc6266.ParseException):
        pyrfc6266.parse(r"""attachment; filename=bar foo=foo """)


def test_greenbytes_attmissingdelim3():
    with pytest.raises(pyrfc6266.ParseException):
        pyrfc6266.parse(r"""attachment filename=bar""")


def test_greenbytes_attreversed():
    with pytest.raises(pyrfc6266.ParseException):
        pyrfc6266.parse(r"""filename=foo.html; attachment""")


def test_greenbytes_attconfusedparam():
    s = r"""attachment; xfilename=foo.html"""
    assert pyrfc6266.parse(s) == (
        "attachment",
        [
            ContentDisposition("xfilename", "foo.html"),
        ],
    )
    assert pyrfc6266.parse_filename(s) is None


def test_greenbytes_attabspath():
    s = r'''attachment; filename="/foo.html"'''
    assert pyrfc6266.parse(s) == (
        "attachment",
        [
            ContentDisposition("filename", "/foo.html"),
        ],
    )
    assert pyrfc6266.parse_filename(s) == "_foo.html"


def test_greenbytes_attabspathwin():
    s = r'''attachment; filename="\\foo.html"'''
    assert pyrfc6266.parse(s) == (
        "attachment",
        [
            ContentDisposition("filename", "\\foo.html"),
        ],
    )
    assert pyrfc6266.parse_filename(s) == "_foo.html"


def test_greenbytes_attcdate():
    assert pyrfc6266.parse(
        r'''attachment; creation-date="Wed, 12 Feb 1997 16:29:51 -0500"'''
    ) == (
        "attachment",
        [
            ContentDisposition("creation-date", "Wed, 12 Feb 1997 16:29:51 -0500"),
        ],
    )


def test_greenbytes_attmdate():
    assert pyrfc6266.parse(
        r'''attachment; modification-date="Wed, 12 Feb 1997 16:29:51 -0500"'''
    ) == (
        "attachment",
        [
            ContentDisposition("modification-date", "Wed, 12 Feb 1997 16:29:51 -0500"),
        ],
    )


def test_greenbytes_dispext():
    assert pyrfc6266.parse(r"""foobar""") == ("foobar", [])


def test_greenbytes_dispextbadfn():
    assert pyrfc6266.parse(r'''attachment; example="filename=example.txt"''') == (
        "attachment",
        [
            ContentDisposition("example", "filename=example.txt"),
        ],
    )


def test_greenbytes_attwithisofn2231iso():
    s = r"""attachment; filename*=iso-8859-1''foo-%E4.html"""
    assert pyrfc6266.parse(s) == (
        "attachment",
        [
            ContentDisposition("filename*", "foo-ä.html"),
        ],
    )
    assert pyrfc6266.parse_filename(s) == "foo-ä.html"


def test_greenbytes_attwithfn2231utf8():
    s = r"""attachment; filename*=UTF-8''foo-%c3%a4-%e2%82%ac.html"""
    assert pyrfc6266.parse(s) == (
        "attachment",
        [
            ContentDisposition("filename*", "foo-ä-€.html"),
        ],
    )
    assert pyrfc6266.parse_filename(s) == "foo-ä-€.html"


def test_greenbytes_attwithfn2231noc():
    assert pyrfc6266.parse(
        r"""attachment; filename*=''foo-%c3%a4-%e2%82%ac.html"""
    ) == ("attachment", [])


def test_greenbytes_attwithfn2231utf8comp():
    s = r"""attachment; filename*=UTF-8''foo-a%cc%88.html"""
    assert pyrfc6266.parse(s) == (
        "attachment",
        [
            ContentDisposition("filename*", "foo-ä.html"),
        ],
    )
    assert pyrfc6266.parse_filename(s) == "foo-ä.html"


def test_greenbytes_attwithfn2231utf8_bad():
    with pytest.raises(pyrfc6266.ParseException):
        pyrfc6266.parse(
            r"""attachment; filename*=iso-8859-1''foo-%c3%a4-%e2%82%ac.html"""
        )


def test_greenbytes_attwithfn2231iso_bad():
    with pytest.raises(pyrfc6266.ParseException):
        pyrfc6266.parse(r"""attachment; filename*=utf-8''foo-%E4.html""")


def test_greenbytes_attwithfn2231ws1():
    with pytest.raises(pyrfc6266.ParseException):
        pyrfc6266.parse(r"""attachment; filename *=UTF-8''foo-%c3%a4.html""")


def test_greenbytes_attwithfn2231ws2():
    s = r"""attachment; filename*= UTF-8''foo-%c3%a4.html"""
    assert pyrfc6266.parse(s) == (
        "attachment",
        [
            ContentDisposition("filename*", "foo-ä.html"),
        ],
    )
    assert pyrfc6266.parse_filename(s) == "foo-ä.html"


def test_greenbytes_attwithfn2231ws3():
    s = r"""attachment; filename* =UTF-8''foo-%c3%a4.html"""
    assert pyrfc6266.parse(s) == (
        "attachment",
        [
            ContentDisposition("filename*", "foo-ä.html"),
        ],
    )
    assert pyrfc6266.parse_filename(s) == "foo-ä.html"


# def test_greenbytes_attwithfn2231quot(): # Disabled due to real-world situation
#     with pytest.raises(pyrfc6266.ParseException):
#         pyrfc6266.parse(r'''attachment; filename*="UTF-8''foo-%c3%a4.html"''')


def test_greenbytes_attwithfn2231quot2():
    with pytest.raises(pyrfc6266.ParseException):
        pyrfc6266.parse(r'''attachment; filename*="foo%20bar.html"''')


def test_greenbytes_attwithfn2231singleqmissing():
    with pytest.raises(pyrfc6266.ParseException):
        pyrfc6266.parse(r"""attachment; filename*=UTF-8'foo-%c3%a4.html""")


def test_greenbytes_attwithfn2231nbadpct1():
    with pytest.raises(pyrfc6266.ParseException):
        pyrfc6266.parse(r"""attachment; filename*=UTF-8''foo%""")


def test_greenbytes_attwithfn2231nbadpct2():
    with pytest.raises(pyrfc6266.ParseException):
        pyrfc6266.parse(r"""attachment; filename*=UTF-8''f%oo.html""")


def test_greenbytes_attwithfn2231dpct():
    s = r"""attachment; filename*=UTF-8''A-%2541.html"""
    assert pyrfc6266.parse(s) == (
        "attachment",
        [
            ContentDisposition("filename*", "A-%41.html"),
        ],
    )
    assert pyrfc6266.parse_filename(s) == "A-%41.html"


def test_greenbytes_attwithfn2231abspathdisguised():
    s = r"""attachment; filename*=UTF-8''%5cfoo.html"""
    assert pyrfc6266.parse(s) == (
        "attachment",
        [
            ContentDisposition("filename*", "\\foo.html"),
        ],
    )
    assert pyrfc6266.parse_filename(s) == "_foo.html"


def test_greenbytes_attfncont():
    s = r'''attachment; filename*0="foo."; filename*1="html"'''
    assert pyrfc6266.parse(s) == (
        "attachment",
        [
            ContentDisposition("filename*0", "foo."),
            ContentDisposition("filename*1", "html"),
        ],
    )
    assert pyrfc6266.parse_filename(s) == "foo.html"


def test_greenbytes_attfncontqs():
    s = r'''attachment; filename*0="foo"; filename*1="\b\a\r.html"'''
    assert pyrfc6266.parse(s) == (
        "attachment",
        [
            ContentDisposition("filename*0", "foo"),
            ContentDisposition("filename*1", "bar.html"),
        ],
    )
    assert pyrfc6266.parse_filename(s) == "foobar.html"


def test_greenbytes_attfncontqs2():
    s = r'''attachment; filename*0="foo"; filename*1="\b\a\n.html"'''
    assert pyrfc6266.parse(s) == (
        "attachment",
        [
            ContentDisposition("filename*0", "foo"),
            ContentDisposition("filename*1", "ban.html"),
        ],
    )
    assert pyrfc6266.parse_filename(s) == "fooban.html"


def test_greenbytes_attfncontenc():
    s = r'''attachment; filename*0*=UTF-8''foo-%c3%a4; filename*1=".html"'''
    assert pyrfc6266.parse(s) == (
        "attachment",
        [
            ContentDisposition("filename*0*", "foo-ä"),
            ContentDisposition("filename*1", ".html"),
        ],
    )
    assert pyrfc6266.parse_filename(s) == "foo-ä.html"


def test_greenbytes_attfncontlz():
    s = r'''attachment; filename*0="foo"; filename*01="bar"'''
    assert pyrfc6266.parse(s) == (
        "attachment",
        [
            ContentDisposition("filename*0", "foo"),
            ContentDisposition("filename*01", "bar"),
        ],
    )
    assert pyrfc6266.parse_filename(s) == "foo"


def test_greenbytes_attfncontnc():
    s = r'''attachment; filename*0="foo"; filename*2="bar"'''
    assert pyrfc6266.parse(s) == (
        "attachment",
        [
            ContentDisposition("filename*0", "foo"),
            ContentDisposition("filename*2", "bar"),
        ],
    )
    assert pyrfc6266.parse_filename(s) == "foo"


def test_greenbytes_attfnconts1():
    s = r'''attachment; filename*1="foo."; filename*2="html"'''
    assert pyrfc6266.parse(s) == (
        "attachment",
        [
            ContentDisposition("filename*1", "foo."),
            ContentDisposition("filename*2", "html"),
        ],
    )
    assert pyrfc6266.parse_filename(s) is None


def test_greenbytes_attfncontord():
    s = r'''attachment; filename*1="bar"; filename*0="foo"'''
    assert pyrfc6266.parse(s) == (
        "attachment",
        [
            ContentDisposition("filename*1", "bar"),
            ContentDisposition("filename*0", "foo"),
        ],
    )
    assert pyrfc6266.parse_filename(s) == "foobar"


def test_greenbytes_attfnboth():
    s = r"""attachment; filename="foo-ae.html"; filename*=UTF-8''foo-%c3%a4.html"""
    assert pyrfc6266.parse(s) == (
        "attachment",
        [
            ContentDisposition("filename", "foo-ae.html"),
            ContentDisposition("filename*", "foo-ä.html"),
        ],
    )
    assert pyrfc6266.parse_filename(s) == "foo-ä.html"


def test_greenbytes_attfnboth2():
    s = r'''attachment; filename*=UTF-8''foo-%c3%a4.html; filename="foo-ae.html"'''
    assert pyrfc6266.parse(s) == (
        "attachment",
        [
            ContentDisposition("filename*", "foo-ä.html"),
            ContentDisposition("filename", "foo-ae.html"),
        ],
    )
    assert pyrfc6266.parse_filename(s) == "foo-ä.html"


# def test_greenbytes_attfnboth3():
#     assert pyrfc6266.parse(r'''attachment; filename*0*=ISO-8859-15''euro-sign%3d%a4; filename*=ISO-8859-1''currency-sign%3d%a4''') == ("attachment", [
#         ContentDisposition("filename*0*", "euro-sign=€"),
#         ContentDisposition("filename", "currency-sign=¤"),
#     ])


def test_greenbytes_attnewandfn():
    s = r'''attachment; foobar=x; filename="foo.html"'''
    assert pyrfc6266.parse(s) == (
        "attachment",
        [
            ContentDisposition("foobar", "x"),
            ContentDisposition("filename", "foo.html"),
        ],
    )
    assert pyrfc6266.parse_filename(s) == "foo.html"


def test_greenbytes_attrfc2047token():
    with pytest.raises(pyrfc6266.ParseException):
        pyrfc6266.parse(r"""attachment; filename==?ISO-8859-1?Q?foo-=E4.html?=""")


def test_greenbytes_attrfc2047quoted():
    assert pyrfc6266.parse(
        r'''attachment; filename="=?ISO-8859-1?Q?foo-=E4.html?="'''
    ) == (
        "attachment",
        [
            ContentDisposition("filename", "=?ISO-8859-1?Q?foo-=E4.html?="),
        ],
    )


def test_requests_from_header():
    response = requests.Response()
    response.url = "https://example.com/path/a_file.txt?token=123"
    response.headers[
        "Content-Disposition"
    ] = 'attachment; filename="different_file.txt"'
    assert pyrfc6266.requests_response_to_filename(response) == "different_file.txt"


def test_requests_from_url():
    response = requests.Response()
    response.url = "https://example.com/path/a_file.txt?token=123"
    assert pyrfc6266.requests_response_to_filename(response) == "a_file.txt"


def test_requests_undiscoverable():
    response = requests.Response()
    response.url = "https://example.com/"
    assert pyrfc6266.requests_response_to_filename(response).startswith("unknown-")


def test_fix_issue_001():
    s = r'''atachment;filename*="utf-8' '100MB.zip"'''
    assert pyrfc6266.parse_filename(s) == '100MB.zip'
