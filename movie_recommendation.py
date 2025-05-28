import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import json
import os
import difflib
import ttkbootstrap as tb
from PIL import Image, ImageTk

class MovieRecommendationSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Movie Recommendation System")
        self.root.state('zoomed')
        self.style = tb.Style(theme="superhero")

        self.movies_file = "movies.json"
        self.movies = self.load_movies()

        self.bg_image = Image.open("movie.jpg")
        self.bg_image = self.bg_image.resize((self.root.winfo_screenwidth(), self.root.winfo_screenheight()), Image.LANCZOS)
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)

        self.canvas = tk.Canvas(root, width=self.root.winfo_screenwidth(), height=self.root.winfo_screenheight())
        self.canvas.pack(fill="both", expand=True)
        self.canvas.create_image(0, 0, image=self.bg_photo, anchor="nw")

        self.add_widgets()

    def add_widgets(self):
        self.frame = ttk.Frame(self.canvas)
        self.canvas.create_window(self.root.winfo_screenwidth()//2, self.root.winfo_screenheight()//2, window=self.frame)

        ttk.Label(self.frame, text="Movie Recommendation System", font=("Helvetica", 16, "bold"), bootstyle="primary").pack(pady=10)

        ttk.Button(self.frame, text="➕ Add Movie", command=self.add_movie_popup, bootstyle="success").pack(pady=10, ipadx=10)
        ttk.Button(self.frame, text="⭐ Recommend Movies", command=self.recommend_movies, bootstyle="warning").pack(pady=10, ipadx=10)
        ttk.Button(self.frame, text="🎭 Suggest by Genre", command=self.suggest_by_genre, bootstyle="info").pack(pady=10, ipadx=10)
        ttk.Button(self.frame, text="📝 Rate & Review", command=self.rate_review_movie, bootstyle="danger").pack(pady=10, ipadx=10)
        ttk.Button(self.frame, text="📜 View All Movies", command=self.view_movies, bootstyle="info").pack(pady=10, ipadx=10)
        ttk.Button(self.frame, text="➖ Minimize", command=self.root.iconify, bootstyle="secondary").pack(pady=10, ipadx=10)

    def load_movies(self):
        if os.path.exists(self.movies_file):
            with open(self.movies_file, 'r') as file:
                return json.load(file)
        return []

    def save_movies(self):
        with open(self.movies_file, 'w') as file:
            json.dump(self.movies, file, indent=4)

    def add_movie_popup(self):
        add_window = tb.Toplevel(self.root)
        add_window.title("Add Movie")
        add_window.state('zoomed')

        center_frame = ttk.Frame(add_window)
        center_frame.place(relx=0.5, rely=0.5, anchor="center")

        ttk.Label(center_frame, text="Title:", bootstyle="info").pack()
        title_entry = ttk.Entry(center_frame, bootstyle="primary")
        title_entry.pack()

        ttk.Label(center_frame, text="Genre:", bootstyle="info").pack()
        genre_entry = ttk.Entry(center_frame, bootstyle="primary")
        genre_entry.pack()

        ttk.Label(center_frame, text="Year:", bootstyle="info").pack()
        year_entry = ttk.Entry(center_frame, bootstyle="primary")
        year_entry.pack()

        ttk.Label(center_frame, text="Rating (1-10):", bootstyle="info").pack()
        rating_entry = ttk.Entry(center_frame, bootstyle="primary")
        rating_entry.pack()

        def save_movie():
            try:
                new_movie = {
                    "title": title_entry.get(),
                    "genre": genre_entry.get(),
                    "year": int(year_entry.get()),
                    "rating": float(rating_entry.get()),
                    "reviews": []
                }
                self.movies.append(new_movie)
                self.save_movies()
                messagebox.showinfo("Success", "Movie added successfully!")
                add_window.destroy()
            except ValueError:
                messagebox.showerror("Error", "Invalid input. Check your fields.")

        ttk.Button(center_frame, text="✔ Add Movie", command=save_movie, bootstyle="success").pack(pady=10)

    def recommend_movies(self):
        recommended = [m for m in self.movies if m["rating"] >= 8]
        self.show_movies_window("Recommended Movies", recommended)

    def suggest_by_genre(self):
        genre_window = tb.Toplevel(self.root)
        genre_window.title("Suggest Movies by Genre")
        genre_window.state('zoomed')

        # Center frame
        center_frame = ttk.Frame(genre_window)
        center_frame.place(relx=0.5, rely=0.5, anchor="center")

        ttk.Label(center_frame, text="Enter Genre:", bootstyle="info").pack(pady=10)
        genre_entry = ttk.Entry(center_frame, bootstyle="primary")
        genre_entry.pack(pady=5)

        def search_genre():
            genre = genre_entry.get().strip()
            if not genre:
                messagebox.showerror("Error", "Please enter a genre.")
                return

            all_genres = list({m["genre"].lower() for m in self.movies})
            best_match = difflib.get_close_matches(genre.lower(), all_genres, n=1, cutoff=0.5)

            if best_match:
                matched_genre = best_match[0]
                filtered_movies = [m for m in self.movies if m["genre"].lower() == matched_genre]
                self.show_movies_window(f"Movies in '{matched_genre.capitalize()}' Genre", filtered_movies)
                genre_window.destroy()
            else:
                messagebox.showinfo("Not Found", f"No close match found for genre '{genre}'")

        ttk.Button(center_frame, text="Search", command=search_genre, bootstyle="success").pack(pady=10)

    def rate_review_movie(self):
        rate_window = tb.Toplevel(self.root)
        rate_window.title("Rate & Review Movie")
        rate_window.state('zoomed')

       
        center_frame = ttk.Frame(rate_window)
        center_frame.place(relx=0.5, rely=0.5, anchor="center")

        ttk.Label(center_frame, text="Enter Movie Title:", bootstyle="info").pack(pady=5)
        title_entry = ttk.Entry(center_frame, width=40, bootstyle="primary")
        title_entry.pack(pady=5)

        ttk.Label(center_frame, text="Enter Rating (1-10):", bootstyle="info").pack(pady=5)
        rating_entry = ttk.Entry(center_frame, width=10, bootstyle="primary")
        rating_entry.pack(pady=5)

        ttk.Label(center_frame, text="Write Review:", bootstyle="info").pack(pady=5)
        review_entry = ttk.Entry(center_frame, width=40, bootstyle="primary")
        review_entry.pack(pady=5)

        def submit_review():
            title = title_entry.get().strip()
            rating_text = rating_entry.get().strip()
            review = review_entry.get().strip()

            if not title or not rating_text or not review:
                messagebox.showerror("Error", "All fields are required.")
                return

            try:
                rating = float(rating_text)
            except ValueError:
                messagebox.showerror("Error", "Rating must be a number.")
                return

            for movie in self.movies:
                if movie["title"].lower() == title.lower():
                    movie["reviews"].append({"rating": rating, "review": review})
                    self.save_movies()
                    messagebox.showinfo("Success", "Review added successfully!")
                    rate_window.destroy()
                    return

            messagebox.showerror("Error", "Movie not found!")

        ttk.Button(center_frame, text="Submit", command=submit_review, bootstyle="success").pack(pady=15)

    def view_movies(self):
        self.show_movies_window("All Movies", self.movies)

    def show_movies_window(self, title, movies):
        window = tb.Toplevel(self.root)
        window.title(title)
        window.state('zoomed')

        main_frame = ttk.Frame(window)
        main_frame.pack(fill="both", expand=True)

       
        canvas = tk.Canvas(main_frame)
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        
      
        content_frame = ttk.Frame(canvas)
        
    
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        
        canvas.create_window((canvas.winfo_width()//2, 0), window=content_frame, anchor="n")

        
        def on_frame_configure(event):
            canvas.configure(scrollregion=canvas.bbox("all"))
            canvas.itemconfig(1, width=event.width)  # Update the width of the canvas window
            
        content_frame.bind("<Configure>", on_frame_configure)
        canvas.bind("<Configure>", lambda e: canvas.itemconfig(1, width=e.width))

        if not movies:
            ttk.Label(content_frame, text="No movies found", bootstyle="danger").pack(pady=20)
        else:
            for movie in movies:
                movie_frame = ttk.Frame(content_frame)
                movie_frame.pack(fill="x", pady=10, padx=20)
                
                ttk.Label(movie_frame, text=f"{movie['title']} ({movie['year']})", 
                         font=("Helvetica", 12, "bold"), bootstyle="primary").pack(anchor="center")
                ttk.Label(movie_frame, text=f"Genre: {movie['genre']} | Rating: ⭐{movie['rating']}").pack(anchor="center")
                
                if movie.get("reviews"):
                    review_frame = ttk.Frame(movie_frame)
                    review_frame.pack(anchor="center", pady=5)
                    ttk.Label(review_frame, text="Reviews:", bootstyle="info").pack(anchor="w")
                    for review in movie["reviews"]:
                        ttk.Label(review_frame, text=f"⭐{review['rating']}: {review['review']}").pack(anchor="w")
                
                ttk.Separator(content_frame).pack(fill="x", pady=5)

if __name__ == "__main__":
    root = tb.Window(themename="superhero")
    app = MovieRecommendationSystem(root)
    root.mainloop()