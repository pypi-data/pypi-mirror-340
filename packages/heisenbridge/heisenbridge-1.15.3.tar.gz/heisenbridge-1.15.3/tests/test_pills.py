from heisenbridge.private_room import parse_irc_formatting


def test_pills():
    # simplified pill expect
    def pill(t):
        return f'<a href="https://matrix.to/#/{t}">{t}</a>'

    def fmt(input):
        pills = {
            "foo": ("foo", "foo"),
            "fo0": ("Fo0", "Fo0"),
            "^foo^": ("^foo^", "^foo^"),
            "[foo]": ("[foo]", "[foo]"),
            "{foo}": ("{foo}", "{foo}"),
        }

        plain, formatted = parse_irc_formatting(input, pills)
        return formatted if formatted else plain

    # must always create a pill
    assert fmt("foo") == pill("foo")
    assert fmt("Fo0") == pill("Fo0")
    assert fmt("foo!") == pill("foo") + "!"
    assert fmt("foo?") == pill("foo") + "?"
    assert fmt("foo bar") == pill("foo") + " bar"
    assert fmt("foo foo foo") == pill("foo") + " " + pill("foo") + " " + pill("foo")
    assert fmt("foo: bar") == pill("foo") + ": bar"
    assert fmt("foo, bar") == pill("foo") + ", bar"
    assert fmt("foo; bar") == pill("foo") + "; bar"
    assert fmt("foo...") == pill("foo") + "..."
    assert fmt("foo bar") == pill("foo") + " bar"
    assert fmt("bar foo.") == "bar " + pill("foo") + "."
    assert fmt("foo. bar") == pill("foo") + ". bar"
    assert fmt("foo? bar") == pill("foo") + "? bar"
    assert fmt("^foo^:") == pill("^foo^") + ":"
    assert fmt("[foo],") == pill("[foo]") + ","
    assert fmt("{foo}?") == pill("{foo}") + "?"

    # anything resembling a working URL should be exempt
    assert fmt("foo.bar") == "foo.bar"
    assert fmt("https://foo.bar/foo?foo=foo&foo=foo#foo") == "https://foo.bar/foo?foo=foo&foo=foo#foo"

    # must never create a pill
    assert fmt("ba.rfoo") == "ba.rfoo"
    assert fmt("barfoo") == "barfoo"
    assert fmt("foo/") == "foo/"
    assert fmt("/foo") == "/foo"
    assert fmt("foo=bar") == "foo=bar"
    assert fmt("foo&bar") == "foo&bar"
    assert fmt("foo#bar") == "foo#bar"
    assert fmt("foo%bar") == "foo%bar"
    assert fmt("äfoo") == "äfoo"
    assert fmt("fooä") == "fooä"
    assert fmt("äfooä") == "äfooä"
