# コンパイラとフラグ
FC = gfortran
FFLAGS = -Wall -O2 -I$(MODDIR)
PYTHON = python3

# ディレクトリ
PROGRAMDIR = program
SRCDIR1 = $(PROGRAMDIR)/mkdata
SRCDIR2 = $(SRCDIR1)/modules
SRCDIR3 = $(PROGRAMDIR)/utils
SRCDIR4 = $(PROGRAMDIR)/mkfig
BINDIR = bin
BUILDDIR = $(BINDIR)/build
OBJDIR = $(BUILDDIR)/obj
MODDIR = $(BUILDDIR)/mod
LOGDIR = log
DATADIR = data
FIGDIR = fig

# 各実行ファイルに対応するソース
TARGETS = vortex wind_profile cartesian
EXECUTABLES = $(addprefix $(BINDIR)/, $(TARGETS))

# 各オブジェクトファイル
OBJ_vortex = $(OBJDIR)/vortex.o
OBJ_wind_profile = $(OBJDIR)/wind_profile.o
OBJ_cartesian = $(OBJDIR)/cartesian.o
OBJ_filepaths = $(OBJDIR)/filepaths.o
OBJ_variables = $(OBJDIR)/variables.o
OBJ_settings = $(OBJDIR)/settings.o
OBJ_constants = $(OBJDIR)/constants.o
OBJ_mod_vortex = $(OBJDIR)/mod_vortex.o

.PHONY: all clean

# デフォルトターゲット
all: init $(EXECUTABLES)

# 個別実行ファイル
$(BINDIR)/vortex: $(OBJ_vortex) $(OBJ_filepaths) $(OBJ_settings) $(OBJ_constants) $(OBJ_mod_vortex)
	$(FC) $(FFLAGS) -o $@ $^

$(BINDIR)/wind_profile: $(OBJ_wind_profile) $(OBJ_filepaths) $(OBJ_settings)
	$(FC) $(FFLAGS) -o $@ $^

$(BINDIR)/cartesian: $(OBJ_cartesian) $(OBJ_filepaths) $(OBJ_variables) $(OBJ_settings) $(OBJ_mod_vortex)
	$(FC) $(FFLAGS) -o $@ $^

# 明示的な依存
$(OBJ_vortex): $(OBJ_filepaths) $(OBJ_settings) $(OBJ_constants) $(OBJ_mod_vortex)
$(OBJ_cartesian): $(OBJ_filepaths) $(OBJ_variables) $(OBJ_settings) $(OBJ_mod_vortex)
$(OBJ_wind_profile): $(OBJ_filepaths)

# オブジェクトファイルのビルドルール
$(OBJDIR)/%.o: $(SRCDIR1)/%.f90 | $(OBJDIR) $(MODDIR)
	$(FC) $(FFLAGS) -c $< -J$(MODDIR) -o $@

$(OBJDIR)/%.o: $(SRCDIR2)/%.f90 | $(OBJDIR) $(MODDIR)
	$(FC) $(FFLAGS) -c $< -J$(MODDIR) -o $@

# ディレクトリの作成
$(OBJDIR):
	mkdir -p $(OBJDIR)

$(MODDIR):
	mkdir -p $(MODDIR)

$(BINDIR):
	mkdir -p $(BINDIR)

init:
	mkdir -p $(BUILDDIR) $(OBJDIR) $(MODDIR) $(BINDIR) $(DATADIR) $(FIGDIR) $(LOGDIR)
	touch $(PROGRAMDIR)/__init__.py
	$(PYTHON) $(SRCDIR3)/write_nml.py

run:
	$(BINDIR)/wind_profile
	$(PYTHON) $(SRCDIR4)/wind_profile.py
	$(BINDIR)/vortex
	$(PYTHON) $(SRCDIR4)/vortex_rz.py
	$(PYTHON) $(SRCDIR4)/vortex_r.py
	$(PYTHON) $(SRCDIR4)/vortex_z.py
	$(BINDIR)/cartesian
	$(PYTHON) $(SRCDIR4)/cart_u.py
	$(PYTHON) $(SRCDIR4)/cart_v.py
	$(PYTHON) $(SRCDIR4)/cart_pre.py
	$(PYTHON) $(SRCDIR4)/cart_tem.py
	$(PYTHON) $(SRCDIR4)/cart_qv.py
	

# クリーン
clean:
	rm -rf $(OBJDIR)/*.o $(MODDIR)/*.mod $(EXECUTABLES)
	rm -rf $(BUILDDIR) $(BINDIR)
	rm -rf $(PROGRAMDIR)/__init__.py
	rm -rf config/param.nml
	rm -rf $(DATADIR)
	rm -rf $(FIGDIR)
	rm -rf $(LOGDIR)