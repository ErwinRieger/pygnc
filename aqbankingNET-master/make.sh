export PKG_CONFIG_PATH="$PREFIX/lib/pkgconfig"
make
make DESTDIR="$PREFIX" install_lib

