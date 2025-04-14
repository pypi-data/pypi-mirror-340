#type: ignore
from dataclasses import dataclass, field
from typing import List
from statistics import mean
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box

console = Console()

@dataclass
class Course:
    name: str
    code: str
    credits: float
    
    def __post_init__(self):
        if not isinstance(self.credits, (int, float)) or self.credits <= 0:
            raise ValueError("Credits must be a positive number")
        if not self.code.isalnum():
            raise ValueError("Course code must be alphanumeric")
        if not self.name.strip():
            raise ValueError("Course name cannot be empty")

@dataclass
class Student:
    name: str
    student_id: int = field(default_factory=lambda: Student._get_next_id())
    _next_id: int = field(default=1, init=False, repr=False)
    
    @classmethod
    def _get_next_id(cls):
        current = cls._next_id
        cls._next_id += 1
        return current
    
    def __post_init__(self):
        if not self.name.strip():
            raise ValueError("Student name cannot be empty")

@dataclass
class Grade:
    student: Student
    course: Course
    score: float

    def __post_init__(self):
        if not isinstance(self.score, (int, float)) or not 0 <= self.score <= 100:
            raise ValueError("Grade must be between 0 and 100")
    
    def letter_grade(self):
        if self.score >= 90:
            return "A"
        elif self.score >= 80:
            return "B"
        elif self.score >= 70:
            return "C"
        elif self.score >= 60:
            return "D"
        else:
            return "F"

@dataclass
class GradeTracker:
    students: List[Student] = field(default_factory=list)
    courses: List[Course] = field(default_factory=list)
    grades: List[Grade] = field(default_factory=list)

    def add_student(self, student: Student):
        self.students.append(student)
        return student

    def add_course(self, course: Course):
        self.courses.append(course)
        return course

    def add_grade(self, student_id: int, course_code: str, score: float):
        student = next((s for s in self.students if s.student_id == student_id), None)
        course = next((c for c in self.courses if c.code == course_code), None)
        
        if not student:
            raise ValueError(f"Student with ID {student_id} not found")
        if not course:
            raise ValueError(f"Course with code {course_code} not found")
        
        grade = Grade(student, course, score)
        self.grades.append(grade)
        return grade

    def get_student_grades(self, student_id: int) -> List[Grade]:
        """Returns a list of grades for a given student."""
        return [grade for grade in self.grades if grade.student.student_id == student_id]

    def calculate_gpa(self, student_id: int) -> float:
        grades = self.get_student_grades(student_id)
        if not grades:
            return 0.0
        
        grade_points = {"A": 4.0, "B": 3.0, "C": 2.0, "D": 1.0, "F": 0.0}
        total_points = 0.0
        total_credits = 0.0
        
        for grade in grades:
            points = grade_points[grade.letter_grade()]
            credits = grade.course.credits
            total_points += points * credits
            total_credits += credits
        
        return round(total_points / total_credits, 2) if total_credits > 0 else 0.0

def display_menu():
    console.print(Panel.fit(
        "[bold cyan]Student Grade Tracker[/bold cyan]\n"
        "1. Add Student\n"
        "2. Add Course\n"
        "3. Add Grade\n"
        "4. Calculate GPA\n"
        "5. List Students\n"
        "6. List Courses\n"
        "7. View Student Grades\n"
        "8. Exit",
        title="Menu",
        border_style="green",
        box=box.ROUNDED
    ))

def display_students(tracker: GradeTracker):
    if not tracker.students:
        console.print("[yellow]No students registered.[/yellow]")
        return
    
    table = Table(title="Students", box=box.SIMPLE, style="cyan")
    table.add_column("ID", justify="center")
    table.add_column("Name", justify="left")
    
    for student in tracker.students:
        table.add_row(str(student.student_id), student.name)
    
    console.print(table)

def display_courses(tracker: GradeTracker):
    if not tracker.courses:
        console.print("[yellow]No courses registered.[/yellow]")
        return
    
    table = Table(title="Courses", box=box.SIMPLE, style="cyan")
    table.add_column("Code", justify="center")
    table.add_column("Name", justify="left")
    table.add_column("Credits", justify="right")
    
    for course in tracker.courses:
        table.add_row(course.code, course.name, f"{course.credits:.1f}")
    
    console.print(table)

def display_grades(tracker: GradeTracker, student_id: int):
    grades = tracker.get_student_grades(student_id)
    student = next((s for s in tracker.students if s.student_id == student_id), None)
    
    if not student:
        console.print(f"[red]Student with ID {student_id} not found.[/red]")
        return
    
    if not grades:
        console.print(f"[yellow]No grades for {student.name} (ID: {student_id}).[/yellow]")
        return
    
    table = Table(title=f"Grades for {student.name} (ID: {student_id})", box=box.SIMPLE, style="cyan")
    table.add_column("Course", justify="left")
    table.add_column("Score", justify="right")
    table.add_column("Letter", justify="center")
    
    for grade in grades:
        table.add_row(grade.course.name, f"{grade.score:.1f}", grade.letter_grade())
    
    console.print(table)

def main():
    tracker = GradeTracker()
    
    while True:
        console.clear()
        display_menu()
        
        choice = console.input("[bold]Enter your choice (1-8): [/bold]")
        
        try:
            if choice == "1":
                name = console.input("[bold]Enter student name: [/bold]").strip()
                if not name:
                    console.print("[red]Name cannot be empty.[/red]")
                    continue
                student = tracker.add_student(Student(name))
                console.print(f"[green]Added student: {student.name} (ID: {student.student_id})[/green]")
            
            elif choice == "2":
                name = console.input("[bold]Enter course name: [/bold]").strip()
                code = console.input("[bold]Enter course code: [/bold]").strip()
                credits_str = console.input("[bold]Enter course credits: [/bold]").strip()
                
                if not name or not code:
                    console.print("[red]Name and code cannot be empty.[/red]")
                    continue
                
                credits = float(credits_str)
                course = tracker.add_course(Course(name, code, credits))
                console.print(f"[green]Added course: {course.name} ({course.code}, {course.credits:.1f} credits)[/green]")
            
            elif choice == "3":
                student_id_str = console.input("[bold]Enter student ID: [/bold]").strip()
                course_code = console.input("[bold]Enter course code: [/bold]").strip()
                score_str = console.input("[bold]Enter grade score (0-100): [/bold]").strip()
                
                student_id = int(student_id_str)
                score = float(score_str)
                grade = tracker.add_grade(student_id, course_code, score)
                console.print(f"[green]Added grade: {grade.score:.1f} ({grade.letter_grade()}) for {grade.student.name} in {grade.course.name}[/green]")
            
            elif choice == "4":
                student_id_str = console.input("[bold]Enter student ID: [/bold]").strip()
                student_id = int(student_id_str)
                gpa = tracker.calculate_gpa(student_id)
                
                student = next((s for s in tracker.students if s.student_id == student_id), None)
                if student:
                    console.print(Panel(
                        f"[bold]GPA for {student.name} (ID: {student_id}): {gpa:.2f}[/bold]",
                        style="cyan",
                        border_style="green",
                        box=box.ROUNDED
                    ))
                else:
                    console.print(f"[red]Student with ID {student_id} not found.[/red]")
            
            elif choice == "5":
                display_students(tracker)
            
            elif choice == "6":
                display_courses(tracker)
            
            elif choice == "7":
                student_id_str = console.input("[bold]Enter student ID: [/bold]").strip()
                student_id = int(student_id_str)
                display_grades(tracker, student_id)
            
            elif choice == "8":
                console.print("[bold magenta]Goodbye![/bold magenta]")
                break
            
            else:
                console.print("[red]Invalid choice. Please enter 1-8.[/red]")
        
        except ValueError as e:
            console.print(f"[red]Error: {str(e)}[/red]")
        
        console.input("[dim]Press Enter to continue...[/dim]")

if __name__ == "__main__":
    main()