SHELL=/bin/csh
GAU_DIR = $(gdvroot)/gdv
GAU_DIRL = $(GAU_DIR)
GAU_DIRA = $(GAU_DIR)
UTIL_NAME = util.a

FLC = flc
#BLAS = -lcxml
#BLAS = -lblas
#BLAS = -lesslp2
BLAS = -lscs_i8
IBM_FC = xlf_r -q64 -qsmp=noauto -qextname -qintsize=8 -qrealsize=8
SGI_FC = f77 -w -i8 -r8 -r8const -mips4 -64 -mp -r10000 -align64 -trapuv -Wl,-Xlocal,tstampc_ -Wl,-Xlocal,savedt_
SGI_FC2 = -lfastm
SUN_FC = f95 -fast -xtypemap=real:64,double:64,integer:64 -xtarget=native -xarch=v9 -xcache=generic
ALP_FC = f90 -O5 -transform_loops -omp -automatic -i8 -r8 -align dcommons \
  -tune host -trapuv -assume noaccuracy_sensitive -math_library fast \
  -reentrancy threaded
LIN_FC = pgf77 -mp -Mnostdlib
PGILIBS = $(PGI)/linux86/lib/libpgthread.a $(PGI)/linux86/lib/libpgc.a $(PGI)/linux86/lib/libpgftnrtl.a $(PGI)/linux86/lib/libpgc.a $(PGI)/linux86/lib/libpgmp.a $(PGI)/linux86/lib/libpgc.a
LIN_FC2 = /usr/local/lib/libf77blas.a /usr/local/lib/libatlas.a $(PGILIBS)
CRY_FC = f90 
CRY_FC2 = -Wl"-M /dev/null -D DUPENTRY=NOTE -D FORCE=OFF -f indef"
HP_FC = f77 +U77
HP_FC2 = -lveclib -lcps -lpthread -lm
PROFFLAG =
#NUTILM = ../nutil/nutil-mark
#NUTIL = ../nutil/*.o
#NUTILL = ../nutill/*.lo ../nutill/*.o
#NUTILLM = ../nutill

FC0 = $(FCN) $(FC) $(PROFFLAG)
FC2 = $(CRY_FC2)
FC1 = $(GAU_DIRL)/$(UTIL_NAME) $(FC2)

.SUFFIXES:
.SUFFIXES: .lo .o .fl .F

.F.o:
	rm -f $*.o
	$(MAKE) -f $(GAU_DIRL)/bsd/gdv.make MAKE='$(MAKE)' GAUDIM='$(GAUDIM)' PROFFLAG='$(PROFFLAG)' `set-mflags` $*.o

.F.lo:
	rm -f $*.fl $*.lo
	$(MAKE) -f $(GAU_DIR)/bsd/gdv.make MAKE='$(MAKE)' PROFFLAG='$(PROFFLAG)' INCDIR=-I. `set-mflags` $*.fl
	mv $*.fl x$*.fl
	$(MAKE) -f $(GAU_DIR)/bsd/gdv.make MAKE='$(MAKE)' PROFFLAG='$(PROFFLAG)' INCDIR=-I. `set-mflags` x$*.lo
	mv x$*.lo $*.lo
	rm -f x$*.fl

all: l118.exe 

bdrys.o:
	gau-get bdrys utilam
	make -f $(GAU_DIRL)/bsd/gdv.make MAKE='$(MAKE)' GAUDIM='$(GAUDIM)' PROFFLAG='$(PROFFLAG)' $*.o
	rm -f bdrys.F

bdam1.o:
	gau-get bdam1 utilam
	make -f $(GAU_DIRL)/bsd/gdv.make MAKE='$(MAKE)' GAUDIM='$(GAUDIM)' PROFFLAG='$(PROFFLAG)' $*.o
	rm -f bdam1.F

clean:
	-rm -f *.a *.o *.f *.fl *.exe

OBJUT = 
OBJPARUT =
OBJLIN = $(GAU_DIRL)/mdutil-linda.o $(GAU_DIRL)/drum.lo \
         $(GAU_DIRL)/evlind.lo $(GAU_DIRL)/chain.lo $(GAU_DIRL)/linint.lo \
	 $(GAU_DIRL)/glini1.lo $(GAU_DIRL)/glinix.lo $(GAU_DIRL)/prlin3.lo \
	 $(GAU_DIRL)/cktspc.lo $(GAU_DIRL)/glin2d.lo \
	 $(GAU_DIRL)/glinco.lo $(GAU_DIRL)/glinfl.lo $(GAU_DIRL)/glinst.lo 

$(COBJS):
	$(MAKE) -f $(GAU_DIRL)/bsd/gdv.make MAKE='$(MAKE)' GAUDIM='$(GAUDIM)' PROFFLAG='$(PROFFLAG)' $*.o

MAIN118 = ml118.o
MAIN118L = $(MAIN118:.o=.lo)
OBJPAR118 =
OBJ118 = velvir.o 
OBJL118 = $(OBJ118) $(OBJPAR118) $(OBJUT) $(OBJPARUT) 
OBJL118L = $(OBJ118) $(OBJPAR118:.o=.lo) $(OBJUT) $(OBJPARUT:.o=.lo) $(COBJS) $(OBJLIN)

l118.exe: $(MAIN118) $(OBJL118) $(NUTILM)
	$(FC0) -g -o l118.exe $(MAIN118) $(OBJL118) $(NUTIL) $(GAU_DIRA)/l118.a $(FC1) $(BLAS)
	gau-fixexe l118.exe

l118.exel: $(MAIN118L) $(OBJL118L) $(NUTILLM)
	$(FLC) -linda link_args "$(FC) $(BLAS) $(FC2)" -o l118.exel $(MAIN118L) \
	  $(OBJL118L) $(NUTILL) $(GAU_DIRL)/l118.a $(FC1)
	gau-fixexe l118.exel

ck118:
	cat $(MAIN118:.o=.F) $(OBJ118:.o=.F) $(OBJPAR118:.o=.F) $(OBJUT:.o=.F) $(NUTIL:.o=.F) >x.x
	checkf x.x x
	rm -f x.x

ml118.F:
	gau-get $(@:.F=) main

NAMEUT = exutil
MAINNUT = $(NAMEUT).o
OBJNUT = 
OBJLNUT = $(OBJNUT) $(OBJUT) $(OBJPARUT) 

$(NAMEUT): $(MAINNUT) $(OBJLNUT) $(NUTILM)
	$(FC0) -g -o $(NAMEUT) $(MAINNUT) $(OBJLNUT) $(NUTIL) $(FC1) $(BLAS)
ckut:
	cat $(MAINNUT:.o=.F) $(OBJNUT:.o=.F) $(OBJPARNUT:.o=.F) $(OBJUT:.o=.F) $(NUTIL:.o=.F) >x.x
	checkf x.x x
	rm -f x.x
