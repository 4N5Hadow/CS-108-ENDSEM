# =============================================================================
# CS108 Exam — Q1: Operation VISION OS
#
# Usage:
#   make          — build everything
#   make shell    — encode inner_score.py + compile NOVA_shell
#   make student  — collect files to hand out to students
#   make clean    — remove build artefacts
# =============================================================================

CXX      := g++
CXXFLAGS := -std=c++17 -O2 -s

SCORE_SRC := inner_score.py
CPP_OUT   := NOVA_shell.cpp
BINARY    := NOVA_shell

STUDENT_DIR   := student_package
STUDENT_FILES := $(STUDENT_DIR)/NOVA_shell \
                 $(STUDENT_DIR)/vision_shell.py \
                 $(STUDENT_DIR)/CS108_VISION_OS_Exam.docx

.PHONY: all shell student clean

all: shell student
	@echo ""
	@echo "  Build complete."
	@echo "  Student files are in: $(STUDENT_DIR)/"

$(CPP_OUT): $(SCORE_SRC) build_nova.py
	@echo "  [1/2] Encoding $(SCORE_SRC) into $(CPP_OUT)..."
	@python3 build_nova.py

$(BINARY): $(CPP_OUT)
	@echo "  [2/2] Compiling $(BINARY)..."
	@$(CXX) $(CXXFLAGS) -o $(BINARY) $(CPP_OUT)
	@echo "        OK — $(BINARY) ready"

shell: $(BINARY)

student: $(BINARY)
	@mkdir -p $(STUDENT_DIR)
	@cp $(BINARY)                 $(STUDENT_DIR)/
	@cp vision_shell.py  $(STUDENT_DIR)/
	@cp CS108_VISION_OS_Exam.docx $(STUDENT_DIR)/
	@echo "  Student package:"
	@ls -1 $(STUDENT_DIR)/ | sed 's/^/    /'

clean:
	@rm -f $(BINARY) $(CPP_OUT)
	@rm -rf $(STUDENT_DIR)
	@echo "  Cleaned."
