"""
COS202 - Personal Pocket CGPA Calculator (PPC)
Author: [Your Name]
Description: A console-based CGPA calculator using Python selection control statements.
             Supports multiple semesters, grade conversion, GPA and CGPA computation,
             and a results summary — all from the command line.
"""

# ──────────────────────────────────────────────────────────────────────────────
#  Grade Scale (Nigerian University System)
# ──────────────────────────────────────────────────────────────────────────────
def get_grade_and_point(score: float):
    """
    Converts a numeric score to a letter grade and grade point
    using the standard Nigerian university grading scale.
    """
    if score >= 70:
        return "A", 5
    elif score >= 60:
        return "B", 4
    elif score >= 50:
        return "C", 3
    elif score >= 45:
        return "D", 2
    elif score >= 40:
        return "E", 1
    else:
        return "F", 0


# ──────────────────────────────────────────────────────────────────────────────
#  Display Helpers
# ──────────────────────────────────────────────────────────────────────────────
DIVIDER = "=" * 60

def print_header():
    print("\n" + DIVIDER)
    print("       🎓  PERSONAL POCKET CGPA CALCULATOR (PPC)")
    print("              COS202 | Python Assignment")
    print(DIVIDER)

def print_grade_scale():
    print("\n  📋  GRADING SCALE (Nigerian University System)")
    print("  " + "-" * 40)
    print(f"  {'Score Range':<20} {'Grade':<10} {'Point'}")
    print("  " + "-" * 40)
    scale = [
        ("70 – 100", "A", 5),
        ("60 – 69",  "B", 4),
        ("50 – 59",  "C", 3),
        ("45 – 49",  "D", 2),
        ("40 – 44",  "E", 1),
        ("0  – 39",  "F", 0),
    ]
    for score_range, grade, point in scale:
        print(f"  {score_range:<20} {grade:<10} {point}")
    print("  " + "-" * 40)

def print_semester_result(semester_num: int, courses: list, gpa: float):
    print(f"\n  📊  Semester {semester_num} Result Summary")
    print("  " + "-" * 56)
    print(f"  {'Course':<22} {'Units':>5}  {'Score':>6}  {'Grade':>5}  {'Points':>6}")
    print("  " + "-" * 56)
    for course in courses:
        name  = course["name"]
        units = course["units"]
        score = course["score"]
        grade = course["grade"]
        gp    = course["grade_point"]
        wgp   = course["weighted_gp"]
        print(f"  {name:<22} {units:>5}  {score:>6.1f}  {grade:>5}  {wgp:>6.1f}")
    print("  " + "-" * 56)
    print(f"  {'Semester GPA':<40} {gpa:.4f}")
    print("  " + "-" * 56)

def get_cgpa_remark(cgpa: float) -> str:
    """Returns the honours class for a given CGPA."""
    if cgpa >= 4.50:
        return "First Class Honours 🏆"
    elif cgpa >= 3.50:
        return "Second Class Upper (2:1) 🥇"
    elif cgpa >= 2.40:
        return "Second Class Lower (2:2) 🥈"
    elif cgpa >= 1.50:
        return "Third Class Honours 🥉"
    elif cgpa >= 1.00:
        return "Pass"
    else:
        return "Fail ❌"


# ──────────────────────────────────────────────────────────────────────────────
#  Input Helpers  (with validation)
# ──────────────────────────────────────────────────────────────────────────────
def input_int(prompt: str, min_val: int = 1, max_val: int = 999) -> int:
    while True:
        try:
            value = int(input(prompt).strip())
            if min_val <= value <= max_val:
                return value
            print(f"  ⚠  Please enter a number between {min_val} and {max_val}.")
        except ValueError:
            print("  ⚠  Invalid input. Please enter a whole number.")

def input_float(prompt: str, min_val: float = 0.0, max_val: float = 100.0) -> float:
    while True:
        try:
            value = float(input(prompt).strip())
            if min_val <= value <= max_val:
                return value
            print(f"  ⚠  Please enter a number between {min_val} and {max_val}.")
        except ValueError:
            print("  ⚠  Invalid input. Please enter a number (e.g. 75 or 68.5).")

def input_yes_no(prompt: str) -> bool:
    while True:
        ans = input(prompt).strip().lower()
        if ans in ("y", "yes"):
            return True
        elif ans in ("n", "no"):
            return False
        print("  ⚠  Please type 'y' for yes or 'n' for no.")


# ──────────────────────────────────────────────────────────────────────────────
#  Core: Collect one semester's data
# ──────────────────────────────────────────────────────────────────────────────
def collect_semester(semester_num: int) -> dict:
    """
    Prompts the user to enter all courses for a semester.
    Returns a dict with the list of courses and the computed GPA.
    """
    print(f"\n{DIVIDER}")
    print(f"  📅  SEMESTER {semester_num} DATA ENTRY")
    print(DIVIDER)

    num_courses = input_int("  How many courses did you offer this semester? ", 1, 20)

    courses       = []
    total_units   = 0
    total_quality = 0.0    # sum of (grade_point × credit_units)

    for i in range(1, num_courses + 1):
        print(f"\n  -- Course {i} of {num_courses} --")
        name  = input(f"  Course name/code (e.g. COS202): ").strip().upper()
        if not name:
            name = f"COURSE{i}"

        units = input_int(f"  Credit units for {name} (1-6): ", 1, 6)
        score = input_float(f"  Score for {name} (0–100): ")

        grade, gp = get_grade_and_point(score)
        weighted  = gp * units

        courses.append({
            "name":        name,
            "units":       units,
            "score":       score,
            "grade":       grade,
            "grade_point": gp,
            "weighted_gp": weighted,
        })

        total_units   += units
        total_quality += weighted

        print(f"  ✅  {name} → Grade: {grade}  |  Grade Point: {gp}  |  Weighted GP: {weighted}")

    gpa = total_quality / total_units if total_units > 0 else 0.0

    return {
        "semester":      semester_num,
        "courses":       courses,
        "total_units":   total_units,
        "total_quality": total_quality,
        "gpa":           gpa,
    }


# ──────────────────────────────────────────────────────────────────────────────
#  Core: Compute CGPA from all semesters
# ──────────────────────────────────────────────────────────────────────────────
def compute_cgpa(semesters: list) -> float:
    """
    CGPA = Total Quality Points across ALL semesters
           ─────────────────────────────────────────
           Total Credit Units across ALL semesters
    """
    total_units   = sum(s["total_units"]   for s in semesters)
    total_quality = sum(s["total_quality"] for s in semesters)
    return total_quality / total_units if total_units > 0 else 0.0


# ──────────────────────────────────────────────────────────────────────────────
#  Final Summary
# ──────────────────────────────────────────────────────────────────────────────
def print_final_summary(student_name: str, semesters: list, cgpa: float):
    print("\n\n" + DIVIDER)
    print("              📋  FINAL CGPA REPORT")
    print(DIVIDER)
    print(f"  Student : {student_name}")
    print(f"  Semesters completed: {len(semesters)}")
    print()

    # Per-semester GPA table
    print(f"  {'Semester':<12} {'Units':>6}  {'Quality Pts':>12}  {'GPA':>8}")
    print("  " + "-" * 44)
    for s in semesters:
        print(f"  {'Semester ' + str(s['semester']):<12} "
              f"{s['total_units']:>6}  "
              f"{s['total_quality']:>12.1f}  "
              f"{s['gpa']:>8.4f}")

    total_units   = sum(s["total_units"]   for s in semesters)
    total_quality = sum(s["total_quality"] for s in semesters)

    print("  " + "-" * 44)
    print(f"  {'TOTAL':<12} {total_units:>6}  {total_quality:>12.1f}  {cgpa:>8.4f}")
    print()
    print(f"  ★  CGPA  :  {cgpa:.4f}  out of  5.00")
    print(f"  ★  CLASS :  {get_cgpa_remark(cgpa)}")
    print(DIVIDER)
    print()


# ──────────────────────────────────────────────────────────────────────────────
#  Main Programme
# ──────────────────────────────────────────────────────────────────────────────
def main():
    print_header()
    print_grade_scale()

    print("\n" + DIVIDER)
    print("  👤  STUDENT INFORMATION")
    print(DIVIDER)
    student_name = input("  Enter your full name: ").strip()
    if not student_name:
        student_name = "Student"

    semesters = []
    semester_num = 1

    # ── Keep adding semesters until the user is done ──
    while True:
        semester_data = collect_semester(semester_num)
        semesters.append(semester_data)

        # Print per-semester result
        print_semester_result(
            semester_data["semester"],
            semester_data["courses"],
            semester_data["gpa"]
        )

        # Show running CGPA after each semester
        current_cgpa = compute_cgpa(semesters)
        print(f"\n  📈  Running CGPA after {semester_num} semester(s): {current_cgpa:.4f}")
        print(f"       Classification: {get_cgpa_remark(current_cgpa)}")

        semester_num += 1

        add_more = input_yes_no("\n  Add another semester? (y/n): ")
        if not add_more:
            break

    # ── Final overall CGPA ──
    final_cgpa = compute_cgpa(semesters)
    print_final_summary(student_name, semesters, final_cgpa)

    # ── Offer to check a hypothetical GPA ──
    if input_yes_no("  Would you like to check what grade a score gives? (y/n): "):
        while True:
            score = input_float("  Enter a score (0–100): ")
            grade, gp = get_grade_and_point(score)
            print(f"  Score {score:.1f}  →  Grade: {grade}  |  Grade Point: {gp}")
            if not input_yes_no("  Check another score? (y/n): "):
                break

    print("\n  ✅  Thank you for using the Pocket CGPA Calculator!")
    print("      Good luck with your studies!\n")


# ──────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    main()
