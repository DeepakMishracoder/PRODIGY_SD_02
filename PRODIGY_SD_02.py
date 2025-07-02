import customtkinter as ctk
import random
import threading
import time

# Set the appearance mode and color theme
ctk.set_appearance_mode("dark") 
ctk.set_default_color_theme("blue") 
class NumberGuessingGame:
    def __init__(self):
        # Initialize the main window
        self.root = ctk.CTk()
        self.root.title("🎯 Number Guessing Game")
        self.root.geometry("500x650")
        self.root.resizable(False, False)
        
        # Game variables - keeping it simple and clean
        self.target_number = None
        self.attempts = 0
        self.min_range = 1
        self.max_range = 100
        self.game_active = False
        
        # Create the beautiful UI
        self.setup_ui()
        self.start_new_game()
        
    def setup_ui(self):
        
        # Main container frame with some padding
        main_frame = ctk.CTkFrame(self.root, corner_radius=0, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Title section - making it pop!
        title_label = ctk.CTkLabel(
            main_frame,
            text="🎯 Guess My Number!",
            font=ctk.CTkFont(size=36, weight="bold"),
            text_color=("#2CC985", "#2FA572")  # Nice gradient-like color
        )
        title_label.pack(pady=(0, 10))
        
        # Subtitle with game info
        self.info_label = ctk.CTkLabel(
            main_frame,
            text="",
            font=ctk.CTkFont(size=16),
            text_color=("gray70", "gray30"),
            wraplength=400
        )
        self.info_label.pack(pady=(0, 30))
        
        # Main game container - this is where the magic happens
        self.game_frame = ctk.CTkFrame(
            main_frame,
            corner_radius=20,
            fg_color=("gray90", "gray13"),
            border_width=2,
            border_color=("gray70", "gray25")
        )
        self.game_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Input section with proper spacing
        input_frame = ctk.CTkFrame(self.game_frame, fg_color="transparent")
        input_frame.pack(pady=30, padx=30, fill="x")
        
        # Input label - nice and clear
        guess_label = ctk.CTkLabel(
            input_frame,
            text="Enter your guess:",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=("gray20", "gray90")
        )
        guess_label.pack(pady=(0, 15))
        
        # The input field - making it nice and tall
        self.guess_entry = ctk.CTkEntry(
            input_frame,
            placeholder_text=f"Number between {self.min_range} and {self.max_range}",
            font=ctk.CTkFont(size=16),
            height=45,  # Nice tall input field!
            border_width=2,
            corner_radius=10
        )
        self.guess_entry.pack(fill="x", pady=(0, 20))
        self.guess_entry.bind("<Return>", lambda event: self.make_guess())  # Enter key support
        
        # Button container for nice layout
        button_frame = ctk.CTkFrame(input_frame, fg_color="transparent")
        button_frame.pack(fill="x")
        
        # Main action buttons with hover effects
        self.guess_button = ctk.CTkButton(
            button_frame,
            text="🎲 Make Guess",
            font=ctk.CTkFont(size=16, weight="bold"),
            height=40,
            corner_radius=10,
            command=self.make_guess,
            hover_color=("#1f6aa5", "#144870")
        )
        self.guess_button.pack(side="left", expand=True, fill="x", padx=(0, 10))
        
        self.new_game_button = ctk.CTkButton(
            button_frame,
            text="🔄 New Game",
            font=ctk.CTkFont(size=16, weight="bold"),
            height=40,
            corner_radius=10,
            command=self.start_new_game,
            fg_color=("gray60", "gray40"),
            hover_color=("gray50", "gray30")
        )
        self.new_game_button.pack(side="right", expand=True, fill="x", padx=(10, 0))
        
        # Feedback section - this is where we show results
        feedback_frame = ctk.CTkFrame(self.game_frame, fg_color="transparent")
        feedback_frame.pack(pady=20, padx=30, fill="both", expand=True)
        
        # Feedback display with nice styling
        self.feedback_label = ctk.CTkLabel(
            feedback_frame,
            text="",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=("gray20", "gray90"),
            wraplength=400,
            justify="center"
        )
        self.feedback_label.pack(pady=20, expand=True)
        
        # Stats display - showing attempts
        self.stats_label = ctk.CTkLabel(
            feedback_frame,
            text="Attempts: 0",
            font=ctk.CTkFont(size=16),
            text_color=("gray40", "gray60")
        )
        self.stats_label.pack(pady=(0, 20))
        
        # Progress bar for visual feedback (optional but cool!)
        self.progress_bar = ctk.CTkProgressBar(
            feedback_frame,
            height=8,
            corner_radius=4,
            progress_color=("#2CC985", "#2FA572")
        )
        self.progress_bar.pack(fill="x", pady=(10, 0))
        self.progress_bar.set(0)
        
    def start_new_game(self):
        """Start a fresh game - reset everything"""
        self.target_number = random.randint(self.min_range, self.max_range)
        self.attempts = 0
        self.game_active = True
        
        # Reset the UI to initial state
        self.guess_entry.delete(0, "end")
        self.guess_entry.configure(state="normal")
        self.guess_button.configure(state="normal")
        
        # Update all the text displays
        self.info_label.configure(
            text=f"I'm thinking of a number between {self.min_range} and {self.max_range}.\nCan you guess what it is?"
        )
        self.feedback_label.configure(
            text="🤔 Ready when you are! Enter your first guess above.",
            text_color=("gray20", "gray90")
        )
        self.stats_label.configure(text="Attempts: 0")
        self.progress_bar.set(0)
        
        # Focus on input for better user experience
        self.guess_entry.focus()
        
    def make_guess(self):
        """Handle the user's guess with lots of validation"""
        if not self.game_active:
            return
            
        # Get and validate the input
        guess_text = self.guess_entry.get().strip()
        if not guess_text:
            self.show_feedback("🤷‍♂️ Please enter a number first!", "orange")
            return
            
        try:
            guess = int(guess_text)
        except ValueError:
            self.show_feedback("🚫 That's not a valid number! Please try again.", "red")
            self.guess_entry.delete(0, "end")
            return
            
        if guess < self.min_range or guess > self.max_range:
            self.show_feedback(f"📏 Please guess between {self.min_range} and {self.max_range}!", "orange")
            self.guess_entry.delete(0, "end")
            return
            
        # Process the valid guess
        self.attempts += 1
        self.stats_label.configure(text=f"Attempts: {self.attempts}")
        
        # Update progress bar based on attempts (just for visual appeal)
        progress = min(self.attempts / 15.0, 1.0)  # Cap at 15 attempts for full bar
        self.progress_bar.set(progress)
        
        # Check the guess and give feedback
        if guess == self.target_number:
            self.handle_correct_guess()
        elif guess < self.target_number:
            self.show_feedback(f"📈 {guess} is too low! Try a higher number.", "blue")
        else:
            self.show_feedback(f"📉 {guess} is too high! Try a lower number.", "purple")
            
        # Clear the input for next guess
        self.guess_entry.delete(0, "end")
        
    def handle_correct_guess(self):
        """Victory! The user got it right"""
        self.game_active = False
        self.guess_entry.configure(state="disabled")
        self.guess_button.configure(state="disabled")
        
        # Celebrate based on performance
        if self.attempts == 1:
            message = f"🎉 INCREDIBLE! You got it in just 1 try!\nThe number was {self.target_number}. You're a mind reader! 🔮"
        elif self.attempts <= 5:
            message = f"🎊 EXCELLENT! You found it in {self.attempts} attempts!\nThe number was {self.target_number}. Great guessing skills! 🎯"
        elif self.attempts <= 10:
            message = f"👏 Well done! You got it in {self.attempts} attempts!\nThe number was {self.target_number}. Nice work! ✨"
        else:
            message = f"🎈 You did it! Found it in {self.attempts} attempts!\nThe number was {self.target_number}. Persistence pays off! 💪"
            
        self.show_feedback(message, "green")
        self.progress_bar.set(1.0)  # Full progress bar for victory!
        
        # Maybe add a little celebration animation
        self.celebrate_victory()
        
    def show_feedback(self, message, color_theme="blue"):
        """Display feedback with color coding"""
        color_map = {
            "green": ("#2CC985", "#2FA572"),
            "red": ("#FF6B6B", "#E74C3C"),
            "blue": ("#3498DB", "#2980B9"),
            "orange": ("#F39C12", "#E67E22"),
            "purple": ("#9B59B6", "#8E44AD")
        }
        
        colors = color_map.get(color_theme, ("#2CC985", "#2FA572"))
        self.feedback_label.configure(text=message, text_color=colors)
        
    def celebrate_victory(self):
        """A little victory animation - because why not?"""
        def animate():
            # Simple color pulse animation
            colors = [("#2CC985", "#2FA572"), ("#FFD700", "#FFA500"), ("#FF69B4", "#FF1493")]
            for _ in range(3):  # Pulse 3 times
                for color in colors:
                    self.feedback_label.configure(text_color=color)
                    time.sleep(0.3)
            # Reset to victory green
            self.feedback_label.configure(text_color=("#2CC985", "#2FA572"))
        
        # Run animation in separate thread so UI doesn't freeze
        animation_thread = threading.Thread(target=animate, daemon=True)
        animation_thread.start()
        
    def run(self):
        """Start the application"""
        self.root.mainloop()

def main():
    """Main function to run the game"""
    # Create and run the game
    game = NumberGuessingGame()
    game.run()

if __name__ == "__main__":
    main()