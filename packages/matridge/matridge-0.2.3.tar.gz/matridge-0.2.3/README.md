# matridge

A
[feature-rich](https://slidge.im/docs/matridge/main/user/features.html)
[Matrix](https://matrix.org) to
[XMPP](https://xmpp.org/) puppeteering
[gateway](https://xmpp.org/extensions/xep-0100.html), based on
[slidge](https://slidge.im) and
[nio](https://matrix-nio.readthedocs.io/).

[![CI pipeline status](https://ci.codeberg.org/api/badges/14069/status.svg)](https://ci.codeberg.org/repos/14069)
[![Chat](https://conference.nicoco.fr:5281/muc_badge/slidge@conference.nicoco.fr)](https://slidge.im/xmpp-web/#/guest?join=slidge@conference.nicoco.fr)
[![PyPI package version](https://badge.fury.io/py/matridge.svg)](https://pypi.org/project/matridge/)

[![Packaging status](https://repology.org/badge/vertical-allrepos/slidge-matridge.svg)](https://repology.org/project/slidge-matridge/versions)


matridge lets you chat with users of Matrix without leaving your favorite XMPP client.

## Quickstart

```sh
docker run codeberg.org/slidge/matridge \  # works with podman too
    --jid matrix.example.org \  # can be whatever you want it to be
    --secret some-secret \  # must match your XMPP server config
    --home-dir /somewhere/writeable  # for data persistence
```

Use the `:latest` tag for the latest release, `:vX.X.X` for release X.X.X, and `:main`
for the bleeding edge.

If you do not like containers, other installation methods are detailed
[in the docs](https://slidge.im/docs/matridge/main/admin/install.html).

## Documentation

Hosted on [codeberg pages](https://slidge.im/docs/matridge/main/).

## Contributing

Contributions are **very** welcome, and we tried our best to make it easy
to start hacking on matridge. See [CONTRIBUTING.md](./CONTRIBUTING.md).
