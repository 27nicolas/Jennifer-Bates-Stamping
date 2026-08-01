import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import os
import threading

from bates_stamper import apply_bates_stamping
from src.tools.create_manifest import create_manifest_from_found_pdfs

STAMPED_FOLDER = 'stamped_documents'

class BatesStamperApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Jennifer Bates Stamping")
        self.root.geometry("600x480")

        self.manifest_path = tk.StringVar()

        # --- Create Manifest Section ---
        manifest_frame = tk.LabelFrame(root, text="Step 1: Create Manifest (Optional)", padx=10, pady=10)
        manifest_frame.pack(padx=10, pady=5, fill="x")

        create_manifest_btn = tk.Button(manifest_frame, text="Find PDFs and Create Manifest", command=self.create_manifest)
        create_manifest_btn.pack(pady=5)

        # --- Process Manifest Section ---
        process_frame = tk.LabelFrame(root, text="Step 2: Stamp Documents", padx=10, pady=10)
        process_frame.pack(padx=10, pady=5, fill="x")

        select_file_btn = tk.Button(process_frame, text="Select Manifest File (.xlsx)", command=self.select_manifest_file)
        select_file_btn.pack(pady=5)

        self.manifest_label = tk.Label(process_frame, textvariable=self.manifest_path)
        self.manifest_label.pack(pady=5)
        self.manifest_path.set("No manifest file selected.")

        self.process_btn = tk.Button(process_frame, text="Upload and Process", command=self.run_processing)
        self.process_btn.pack(pady=10)

        # Add progress bar
        self.progress_bar = ttk.Progressbar(process_frame, orient='horizontal', length=100, mode='determinate')
        self.progress_bar.pack(pady=5, fill='x', padx=5)

        # --- Output/Log Section ---
        log_frame = tk.LabelFrame(root, text="Processing Log", padx=10, pady=10)
        log_frame.pack(padx=10, pady=10, fill="both", expand=True)

        self.log_text = scrolledtext.ScrolledText(log_frame, wrap=tk.WORD, state='disabled', height=10)
        self.log_text.pack(fill="both", expand=True)

    def log(self, message, level='info'):
        self.log_text.config(state='normal')
        self.log_text.insert(tk.END, f"{message}\n")
        self.log_text.config(state='disabled')
        self.log_text.see(tk.END)

    def create_manifest(self):
        search_directory = filedialog.askdirectory(
            title="Select Folder to Search for PDFs"
        )
        if not search_directory:
            self.log("Manifest creation cancelled: No folder selected.")
            return

        def task():
            try:
                output_filename = 'new_bates_manifest.xlsx'
                
                # Pass the GUI's log method as the logger
                success = create_manifest_from_found_pdfs(
                    search_directory, 
                    output_filename,
                    logger=self.log
                )
                
                self.log(f"Manifest creation process finished.")
                if success:
                    self.root.after(0, lambda: messagebox.showinfo("Success", f"Manifest '{output_filename}' created successfully in the application folder."))
                    self.manifest_path.set(os.path.abspath(output_filename))
                    self.log(f"Manifest file automatically selected: {output_filename}")
                else:
                    self.root.after(0, lambda: messagebox.showinfo("Info", f"No PDF files were found in the selected directory:\n{search_directory}"))

            except Exception as e:
                self.log(f"Failed to create manifest: {e}")
                self.root.after(0, lambda: messagebox.showerror("Error", f"Failed to create manifest: {e}"))

        threading.Thread(target=task, daemon=True).start()

    def select_manifest_file(self):
        filepath = filedialog.askopenfilename(
            title="Select Manifest File",
            filetypes=(("Excel files", "*.xlsx"), ("All files", "*.*"))
        )
        if filepath:
            self.manifest_path.set(filepath)
            self.log(f"Selected manifest: {filepath}")

    def run_processing(self):
        manifest = self.manifest_path.get()
        if not manifest or "No manifest file selected" in manifest:
            messagebox.showwarning("Warning", "Please select a manifest file first.")
            return

        if not os.path.exists(manifest):
            messagebox.showerror("Error", f"Manifest file not found:\n{manifest}")
            return

        # Disable button and reset progress bar
        self.process_btn.config(state='disabled')
        self.progress_bar['value'] = 0
        self.root.update_idletasks()

        threading.Thread(target=self.process_files, args=(manifest,), daemon=True).start()

    def update_progress(self, current, total):
        """Callback to update the progress bar from a thread."""
        if total > 0:
            percentage = (current / total) * 100
            self.progress_bar['value'] = percentage
            self.root.update_idletasks()

    def process_files(self, manifest_path):
        self.log("Starting Bates stamping process...")
        try:
            if not os.path.exists(STAMPED_FOLDER):
                os.makedirs(STAMPED_FOLDER)
                self.log(f"Created output directory: {STAMPED_FOLDER}")

            # Define a thread-safe callback
            def progress_callback(current, total):
                self.root.after(0, self.update_progress, current, total)

            processed_files, errors = apply_bates_stamping(
                manifest_path,
                STAMPED_FOLDER,
                progress_callback=progress_callback
            )
            
            self.root.after(0, self.show_processing_results, processed_files, errors)

        except Exception as e:
            self.log(f"An error occurred during processing: {e}")
            self.root.after(0, lambda: messagebox.showerror("Processing Error", f"An unexpected error occurred: {e}"))
            # Re-enable button on error
            self.root.after(0, lambda: self.process_btn.config(state='normal'))

    def show_processing_results(self, processed_files, errors):
        # Re-enable the button
        self.process_btn.config(state='normal')

        success_msg = f"Successfully stamped {len(processed_files)} files."
        self.log(success_msg)

        if errors:
            error_summary = f"{len(errors)} errors occurred."
            self.log(error_summary)
            for error in errors:
                self.log(f"ERROR: {error}")
            messagebox.showwarning("Processing Complete with Errors", f"{success_msg}\n\n{error_summary}\n\nSee log for details.")
        else:
            # Set progress to 100 on full success
            self.progress_bar['value'] = 100
            messagebox.showinfo("Success", f"{success_msg}\n\nStamped files are in the '{STAMPED_FOLDER}' directory.")
        
        self.log("Processing complete.")

if __name__ == '__main__':
    root = tk.Tk()
    app = BatesStamperApp(root)
    root.mainloop()