import tkinter as tk
from tkinter import messagebox
import random
from PIL import Image, ImageTk # Pillow 라이브러리 임포트

# 기존 로직 재사용
def generate_winning_numbers():
    numbers = list(range(1, 46))
    random.shuffle(numbers)
    winning_numbers = sorted(numbers[:6])
    bonus_number = numbers[6]
    return winning_numbers, bonus_number

def check_rank(user_numbers, winning_numbers, bonus_number):
    matched_count = len(set(user_numbers) & set(winning_numbers))
    bonus_matched = bonus_number in user_numbers

    if matched_count == 6:
        return "1등"
    elif matched_count == 5 and bonus_matched:
        return "2등"
    elif matched_count == 5:
        return "3등"
    elif matched_count == 4:
        return "4등"
    elif matched_count == 3:
        return "5등"
    else:
        return "꽝"

class LottoSimulatorApp:
    def __init__(self, master):
        self.master = master
        master.title("로또 시뮬레이터")

        self.winning_numbers = []
        self.bonus_number = 0
        self.user_numbers = [] # 사용자 번호를 저장할 리스트

        # 배경 이미지 설정
        try:
            image_path = "D:\\Download\\Image_fx (1).jpg"
            self.bg_image = Image.open(image_path)
            # 윈도우 크기에 맞게 이미지 크기 조절
            self.bg_image = self.bg_image.resize((800, 500), Image.LANCZOS) # 윈도우 크기 800x500에 맞춤
            self.bg_photo = ImageTk.PhotoImage(self.bg_image)

            self.bg_label = tk.Label(master, image=self.bg_photo)
            self.bg_label.place(x=0, y=0, relwidth=1, relheight=1) # 윈도우 전체를 덮도록 배치
            self.bg_label.lower() # 다른 위젯들 뒤로 보내기
        except FileNotFoundError:
            messagebox.showerror("오류", f"이미지 파일을 찾을 수 없습니다: {image_path}")
            self.bg_photo = None
        except Exception as e:
            messagebox.showerror("오류", f"이미지 로딩 중 오류 발생: {e}")
            self.bg_photo = None

        # 모든 UI 요소를 담을 메인 프레임 생성 및 중앙 배치
        self.content_frame = tk.Frame(master, bg="#F0F0F0", bd=5, relief="raised") # 연한 회색 배경, 테두리
        self.content_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER) # 중앙 정렬

        # 당첨 번호 표시 영역 (Canvas)
        tk.Label(self.content_frame, text="당첨 번호:", font=("Arial", 12, "bold"), bg="#F0F0F0").grid(row=0, column=0, columnspan=7, pady=5)
        self.winning_canvas = tk.Canvas(self.content_frame, width=450, height=60, bg="white", bd=2, relief="groove")
        self.winning_canvas.grid(row=1, column=0, columnspan=7, pady=10)

        # 사용자 번호 입력 및 표시 영역
        tk.Label(self.content_frame, text="내 번호:", font=("Arial", 12, "bold"), bg="#F0F0F0").grid(row=2, column=0, columnspan=7, pady=5)
        
        self.user_input_frame = tk.Frame(self.content_frame, bg="#F0F0F0")
        self.user_input_frame.grid(row=3, column=0, columnspan=7, pady=5)

        tk.Label(self.user_input_frame, text="숫자 입력 (1-45):", bg="#F0F0F0").pack(side=tk.LEFT, padx=5)
        self.user_entry = tk.Entry(self.user_input_frame, width=5)
        self.user_entry.pack(side=tk.LEFT, padx=5)
        self.user_entry.bind("<Return>", lambda event: self.add_user_number()) # 엔터 키로 번호 추가

        self.add_number_btn = tk.Button(self.user_input_frame, text="번호 추가", command=self.add_user_number)
        self.add_number_btn.pack(side=tk.LEFT, padx=5)

        self.clear_my_numbers_btn = tk.Button(self.user_input_frame, text="내 번호 지우기", command=self.clear_user_numbers)
        self.clear_my_numbers_btn.pack(side=tk.LEFT, padx=5)

        self.user_numbers_canvas = tk.Canvas(self.content_frame, width=450, height=60, bg="white", bd=2, relief="groove")
        self.user_numbers_canvas.grid(row=4, column=0, columnspan=7, pady=10)

        # 버튼
        self.generate_winning_btn = tk.Button(self.content_frame, text="당첨 번호 생성", command=self.generate_winning_numbers_gui)
        self.generate_winning_btn.grid(row=5, column=0, columnspan=3, pady=10)

        self.generate_my_numbers_btn = tk.Button(self.content_frame, text="내 번호 자동 생성", command=self.generate_my_numbers_gui)
        self.generate_my_numbers_btn.grid(row=5, column=3, columnspan=3, pady=10)

        self.check_numbers_btn = tk.Button(self.content_frame, text="결과 확인", command=self.check_numbers)
        self.check_numbers_btn.grid(row=6, column=0, columnspan=6, pady=10)

        # 결과 표시 영역
        self.result_label = tk.Label(self.content_frame, text="결과: ", font=("Arial", 16, "bold"), bg="#F0F0F0")
        self.result_label.grid(row=7, column=0, columnspan=7, pady=20)

    def _draw_ball(self, canvas, x_center, y_center, number, color):
        radius = 20
        x0 = x_center - radius
        y0 = y_center - radius
        x1 = x_center + radius
        y1 = y_center + radius

        # 3D 효과를 위한 그림자 및 하이라이트
        canvas.create_oval(x0 + 2, y0 + 2, x1 + 2, y1 + 2, fill="#888888", outline="", tags="ball") # 그림자
        canvas.create_oval(x0, y0, x1, y1, fill=color, outline="black", width=1, tags="ball") # 기본 공
        canvas.create_oval(x0 + radius * 0.2, y0 + radius * 0.2, x0 + radius * 0.8, y0 + radius * 0.8, 
                           fill="white", outline="", stipple="gray50", tags="ball") # 하이라이트

        canvas.create_text(x_center, y_center, text=str(number), font=("Arial", 12, "bold"), fill="black", tags="ball")

    def _redraw_user_numbers(self):
        self.user_numbers_canvas.delete("all")
        colors = ["red", "orange", "yellow"]
        x_start = 25
        y_center = 30
        ball_spacing = 50

        for i, num in enumerate(sorted(self.user_numbers)):
            color = random.choice(colors)
            x_center = x_start + i * ball_spacing
            self._draw_ball(self.user_numbers_canvas, x_center, y_center, num, color)

    def add_user_number(self):
        try:
            num_str = self.user_entry.get()
            num = int(num_str)
            self.user_entry.delete(0, tk.END)

            if not 1 <= num <= 45:
                messagebox.showerror("입력 오류", "숫자는 1에서 45 사이여야 합니다.")
            elif num in self.user_numbers:
                messagebox.showerror("입력 오류", "이미 추가된 숫자입니다.")
            elif len(self.user_numbers) >= 6:
                messagebox.showwarning("경고", "최대 6개의 숫자만 추가할 수 있습니다.")
            else:
                self.user_numbers.append(num)
                self.user_numbers.sort()
                self._redraw_user_numbers()
        except ValueError:
            messagebox.showerror("입력 오류", "유효한 숫자를 입력해주세요.")

    def clear_user_numbers(self):
        self.user_numbers = []
        self._redraw_user_numbers()
        self.result_label.config(text="결과: ")

    def generate_winning_numbers_gui(self):
        self.winning_numbers, self.bonus_number = generate_winning_numbers()
        self.winning_canvas.delete("all") # 이전 그림 삭제

        colors = ["red", "orange", "yellow"]
        x_start = 25 # 첫 번째 공의 시작 x 위치
        y_center = 30 # 모든 공의 y 위치
        ball_spacing = 50 # 공 지름 + 간격

        # 당첨 번호 6개 그리기
        for i, num in enumerate(self.winning_numbers):
            color = random.choice(colors)
            x_center = x_start + i * ball_spacing
            self._draw_ball(self.winning_canvas, x_center, y_center, num, color)

        # '+' 기호 그리기
        x_plus = x_start + 5 * ball_spacing + 25 + 10 # 6번째 공의 오른쪽 끝 + 간격
        self.winning_canvas.create_text(x_plus, y_center, text="+ ", font=("Arial", 18, "bold"), fill="black")

        # 보너스 번호 그리기
        color = random.choice(colors)
        x_bonus = x_plus + 25 + 10 # '+' 기호의 오른쪽 끝 + 간격
        self._draw_ball(self.winning_canvas, x_bonus, y_center, self.bonus_number, color)

        self.result_label.config(text="결과: ") # 결과 초기화

    def generate_my_numbers_gui(self):
        self.user_numbers = [] # 기존 번호 초기화
        numbers = list(range(1, 46))
        random.shuffle(numbers)
        for num in sorted(numbers[:6]):
            self.user_numbers.append(num)
        self._redraw_user_numbers()

    def check_numbers(self):
        if not self.winning_numbers:
            messagebox.showwarning("경고", "먼저 당첨 번호를 생성해주세요!")
            return

        if len(self.user_numbers) != 6:
            messagebox.showwarning("경고", "내 번호 6개를 모두 입력해주세요!")
            return

        rank = check_rank(self.user_numbers, self.winning_numbers, self.bonus_number)
        self.result_label.config(text=f"결과: {rank}")


if __name__ == "__main__":
    root = tk.Tk()
    # 윈도우 크기 설정 (배경 이미지 크기에 맞게 조정)
    root.geometry("800x500") 
    root.resizable(False, False) # 윈도우 크기 조절 불가
    app = LottoSimulatorApp(root)
    root.mainloop()
