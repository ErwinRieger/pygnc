# it is HIGHLY RECOMMENDED you leave DESTDIR to /usr, else you need LOTS of
# adjustements in this Makefile to get it working
DESTDIR=/usr
# specify where is monos GAC
GAC_ROOT=$(DESTDIR)/lib
# might be overriden to lib64 
LIBDIR=lib
PCDIR=$(DESTDIR)/$(LIBDIR)/pkgconfig

GWENHYWFAR_CFLAGS=$(shell pkg-config --cflags gwenhywfar)
GWENHYWFAR_LDFLAGS=$(shell pkg-config --libs gwenhywfar)
AQBANKING_CFLAGS=$(shell pkg-config --cflags aqbanking)
AQBANKING_LDFLAGS=$(shell pkg-config --libs aqbanking)
# we HAVE to avoid dots in the .so because windows does not append .dll if 
# there is already a dot in the name within the DllImport parameter
AQBANKING_VERSION=$(shell pkg-config --modversion aqbanking)
AQBANKING_MAJOR=$(shell echo -n $(AQBANKING_VERSION) | cut -f1 -d'.')

NAMESPACE=AqBanking

SWIG=$(shell which swig)
GMCS=$(shell which gmcs)
CC=$(shell which cc)

# input swig interface file which contains wrapper specification
SWIG_INTERFACE=aqbanking.i

# name of target native wrapper library
# on linux mono expects the library to have a 'lib' prefix and .so suffix
WRAPPER_NAME=aqbankingNET-native
WRAPPER_GENERIC_ALIAS=lib$(WRAPPER_NAME).so
WRAPPER_MAJOR_ALIAS=$(WRAPPER_GENERIC_ALIAS).$(AQBANKING_MAJOR)
WRAPPER_LIB=lib$(WRAPPER_NAME).so.$(AQBANKING_VERSION)

CIL_NAME=aqbankingNET$(AQBANKING_MAJOR)
CIL_DLL=$(CIL_NAME).dll
BUILD_OUTPUT_PATH=bin
CS_OUTPUT_PATH=csharp-tmp

# Flags for compiling & linking into a shared .so
CFLAGS=-Wno-deprecated-declarations -fPIC -shared -Wl,-soname,$(WRAPPER_MAJOR_ALIAS)

all: checks gen_wrapper build_cswrapper build_wrapper 

checks:
	@which gmcs > /dev/null
	@which swig > /dev/null
	@which gcc > /dev/null
	@which pkg-config > /dev/null

gen_wrapper:	$(SWIG_INTERFACE)
	### Autogenerate C# wrappers from Aqbanking & Gwenhywfar headers
	@mkdir -p $(CS_OUTPUT_PATH) 
	$(SWIG) $(AQBANKING_CFLAGS) $(GWENHYWFAR_CFLAGS) \
		-outdir $(CS_OUTPUT_PATH) \
		-dllimport $(WRAPPER_NAME) \
		-namespace $(NAMESPACE) \
		-csharp $(SWIG_INTERFACE)

build_cswrapper:
	@mkdir -p $(BUILD_OUTPUT_PATH)
	@# Compile the .cs files and sign with the mono (not so) private key
	$(GMCS) -t:library -keyfile:mono.snk -out:$(BUILD_OUTPUT_PATH)/$(CIL_DLL) $(CS_OUTPUT_PATH)/*.cs

build_wrapper:
	### Compiling the C wrapper libary: $(WRAPPER_LIB)
	@# order is VERY important - some distros (like SUSE Buildservice) fail
	@# if the external CFLAGS & LDFLAGS are placed before the .c file!
	$(CC) $(CFLAGS) -o $(BUILD_OUTPUT_PATH)/$(WRAPPER_LIB) aqbanking_wrap.c \
		$(GWENHYWFAR_CFLAGS) $(AQBANKING_CFLAGS) \
		$(GWENHYWFAR_LDFLAGS) $(AQBANKING_LDFLAGS) 

install:
	### Copying $(WRAPPER_LIB) to $(DESTDIR)/$(LIBDIR)/
	install -D $(BUILD_OUTPUT_PATH)/$(WRAPPER_LIB) $(DESTDIR)/$(LIBDIR)/$(WRAPPER_LIB)
	rm -rf $(DESTDIR)/$(LIBDIR)/$(WRAPPER_MAJOR_ALIAS)
	ln -s $(DESTDIR)/$(LIBDIR)/$(WRAPPER_LIB)  $(DESTDIR)/$(LIBDIR)/$(WRAPPER_MAJOR_ALIAS)
	rm -rf $(DESTDIR)/$(LIBDIR)/$(WRAPPER_GENERIC_ALIAS)
	ln -s $(DESTDIR)/$(LIBDIR)/$(WRAPPER_LIB)  $(DESTDIR)/$(LIBDIR)/$(WRAPPER_GENERIC_ALIAS)

	# in rpm builds its likely $(DESTDIR)mono/gac does not exist, so create it
	mkdir -p $(GAC_ROOT)/mono/gac/
	### Installing $(CIL_DLL) to global assembly cache (GAC)
	gacutil -package aqbankingNET -i $(BUILD_OUTPUT_PATH)/$(CIL_DLL) -root $(GAC_ROOT)
	### Copying .pc to pkg-config directory at $(PCDIR)
	mkdir -p $(PCDIR)
	install -D aqbankingNET.pc $(PCDIR)

uninstall:
	### removing $(DESTDIR)/lib/$(WRAPPER_LIB)
	rm -rf $(DESTDIR)/$(LIBDIR)/$(WRAPPER_LIB)
	rm -rf $(DESTDIR)/$(LIBDIR)/$(WRAPPER_GENERIC_ALIAS)
	rm -rf $(DESTDIR)/$(LIBDIR)/$(WRAPPER_MAJOR_ALIAS)
	### Uninstalling $(CIL_NAME) from global assembly cache (GAC)	
	gacutil -u $(CIL_NAME)
	rm -rf $(GAC_ROOT)/mono/aqbankingNET/

clean: 
	@rm -rf *.o *.c $(CS_OUTPUT_PATH)
	@rm -rf *.so
	@rm -rf *.dll *.tmp $(BUILD_OUTPUT_PATH)
