import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog

class PerformanceReport:
    def __init__(self):
        self.time_slot = ""
        self.results = []
        self.overall_quality = 0.0
        self.total_ops_error = 0.0
        self.invalid_destination = 0.0

    def breaknow(self):
        if self.time_slot in ["1", "1st"]:
            self.results.append("12:30am-3:30am")
            self.results.append("Gap errors due to culling package singulation: Autocut Sev Ticket >0.5%. Goal <0.3%")
        elif self.time_slot in ["2", "2nd"]:
            self.results.append("3:30am-5:30am")
            self.results.append("Gap errors due to culling package singulation: Autocut Sev Ticket >0.5%. Goal <0.3%")

    def gather_data(self, label):
        count = simpledialog.askinteger(f"{label}", f"What is the request count for {label}?")
        gap = simpledialog.askfloat(f"{label}", f"What is the Gap error percentage for {label}?")
        pph = simpledialog.askinteger(f"{label}", f"What is max PPH for {label}?")
        status = "❌" if gap > 0.3 else "✅"
        result = f"{label} - {gap:.2f}% out of {count:,} {status} Max PPH {pph:,}"
        self.results.append(result)

    def gather_overall_quality_data(self):
        self.overall_quality = simpledialog.askfloat("Overall Quality", "Enter Overall Quality (%)")
        self.total_ops_error = simpledialog.askfloat("Total Ops Error", "Enter Total Ops Error (%)")
        self.invalid_destination = simpledialog.askfloat("Invalid Destination", "Enter Invalid Destination (%)")
        status = "❌" if self.overall_quality < 97 else "✅"
        overall_result = (
            f"Overall Quality (Goal >97%) - {self.overall_quality:.2f}% {status} - "
            f"Total Ops Error {self.total_ops_error:.2f}% (Invalid Destination {self.invalid_destination:.3f}%)"
        )
        self.results.append(overall_result)

    def save_results(self):
        with open("performance_report.txt", "w") as file:
            for result in self.results:
                file.write(result + "\n")
        messagebox.showinfo("Saved", "Results have been saved to performance_report.txt")

    def main(self):
        root = tk.Tk()
        root.withdraw()  # Hide the root window

        self.time_slot = simpledialog.askstring("Input", "1st or 2nd break?").strip().lower()
        self.breaknow()

        self.gather_data("AB")
        self.gather_data("CD")
        self.gather_data("EG")
        self.gather_overall_quality_data()

        results_window = tk.Toplevel(root)
        results_window.title("Results")

        results_text = tk.Text(results_window, wrap='word', height=15, width=80)
        results_text.pack(padx=10, pady=10)
        for result in self.results:
            results_text.insert(tk.END, result + "\n")

        save_button = tk.Button(results_window, text="Save Results", command=self.save_results)
        save_button.pack(pady=10)

        root.mainloop()

if __name__ == "__main__":
    report = PerformanceReport()
    report.main()
