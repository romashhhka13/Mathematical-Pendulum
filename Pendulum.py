import tkinter as tk
import numpy as np
import time

from tkinter import ttk
from tkinter import messagebox as mb
from random import randint


class Pendulum:
    def __init__(self):

        self.color1 = 'plum'
        self.color2 = '#EDAEED'
        self.color3 = '#2D0731'
        self.color4 = '#68456B'

        self.width_root = 750
        self.height_root = 600
        self.root = tk.Tk()
        self.root.title("Mathematical pendulum")
        self.root.geometry(f"{self.width_root}x{self.height_root}+"
                           f"{int((self.root.winfo_screenwidth()-self.width_root)/2)}+"
                           f"{int((self.root.winfo_screenheight()-self.height_root)/3)}")
        self.root.resizable(width=False, height=False)

        # creating frames for Pendulum and User
        self.frm1 = tk.Canvas(self.root, bg=self.color1, highlightthickness=0)
        self.frm1.place(relx=0, rely=0, relheight=0.7, relwidth=1)

        self.frm2 = tk.Frame(self.root, bg=self.color2)
        self.frm2.place(relx=0, rely=0.7, relheight=0.3, relwidth=1)

        self.frame_win = tk.Frame(self.root, bg=self.color1)
        self.frame_win.configure(highlightbackground=self.color2, highlightthickness=2, relief='groove')

        self.label_win_title = tk.Label(self.frame_win, bg=self.color1, fg=self.color3)
        self.label_win_title.configure(text='ПОБЕДА!', font=("Arial black", 14), anchor='center')
        self.label_win_title.place(relx=0, rely=0, relwidth=1, relheight=0.12)

        self.label_win_text = tk.Label(self.frame_win, bg=self.color1, fg=self.color3)
        self.label_win_text.configure(font=("Arial", 14), anchor='center')
        self.label_win_text.place(relx=0, rely=0.12, relwidth=1, relheight=0.68)

        self.frame_over = tk.Frame(self.root, bg=self.color1)
        self.frame_over.configure(highlightbackground=self.color2, highlightthickness=2, relief='groove')

        self.label_over_title = tk.Label(self.frame_over, bg=self.color1, fg=self.color3)
        self.label_over_title.configure(text='ПОРАЖЕНИЕ :(', font=("Arial black", 14), anchor='center')
        self.label_over_title.place(relx=0, rely=0, relwidth=1, relheight=0.12)

        self.label_over_text = tk.Label(self.frame_over, bg=self.color1, fg=self.color3)
        self.label_over_text.configure(font=("Arial", 14), anchor='center')
        self.label_over_text.place(relx=0, rely=0.12, relwidth=1, relheight=0.68)

        image_question = tk.PhotoImage(file='question.png')
        self.label_question = tk.Label(self.root, bg=self.color2)
        self.label_question.configure(image=image_question, cursor='hand2')

        # paste blur background
        self.blur_image1 = tk.PhotoImage(file="blur.png")
        self.background = self.frm1.create_image(375, int((600 * 0.7 / 2)), anchor='center', image=self.blur_image1)

        self.blur_image2 = tk.PhotoImage(file="blur1.png")
        self.label_image = tk.Label(self.frm2, image=self.blur_image2)
        self.label_image.place(x=0, y=0, relheight=1, relwidth=1)

        self.meters = None
        self.length_thread = None
        self.mass_pendulum = None
        self.radius_ball = None
        self.angle_deflection = None
        self.g = None
        self.acceleration = None
        self.Oscillation_period = None
        self.Cyclic_frequency = None

        self.stopwatch_begin = 0
        self.stopwatch_end = 0
        self.id_update_stopwatch = None
        self.id_move_pendulum = None

        self.coordinates_center = [self.width_root / 2, self.height_root * 0.05]
        self.thread = None
        self.ball = None

        # Drawing Bracing
        Bracing = self.frm1.create_line([0, self.coordinates_center[1]],
                                        [self.width_root, self.coordinates_center[1]],
                                        fill='purple', width=2)

        # drawing center_point
        center_point = self.frm1.create_oval([self.coordinates_center[0] - 5,
                                              self.coordinates_center[1] - 5],
                                             [self.coordinates_center[0] + 5,
                                              self.coordinates_center[1] + 5],
                                             fill='purple')

        style = ttk.Style()
        style.theme_create("my_style", parent="default", settings={
            "TEntry": {
                "configure": {"padding": [10, 0, 0, 0],
                              "insertwidth": 2,
                              "fieldbackground": self.color1,
                              "borderwidth": 2,
                              "font": ("Arial", 14, 'bold')},
                "map": {"fieldbackground": [('focus', self.color1), ('!focus', self.color2)]}},
        })
        style.theme_use("my_style")


        # create label to count time
        self.ms = tk.StringVar(value='0')
        self.label_ms = tk.Label(self.root, bg=self.color1, textvariable=self.ms)
        self.label_ms.configure(font=("Arial", 12, 'bold'), anchor='s', fg=self.color3)

        self.label_comma = tk.Label(self.root, bg=self.color1, text=',')
        self.label_comma.configure(font=("Arial", 12, 'bold'), anchor='s', fg=self.color3)


        self.sec = tk.StringVar(value='00')
        self.label_sec = tk.Label(self.root, bg=self.color1, textvariable=self.sec)
        self.label_sec.configure(font=("Arial", 12, 'bold'), anchor='s', fg=self.color3)

        self.label_colon = tk.Label(self.root, bg=self.color1, text=':')
        self.label_colon.configure(font=("Arial", 12, 'bold'), anchor='s', fg=self.color3)

        self.min = tk.StringVar(value='00')
        self.label_min = tk.Label(self.root, bg=self.color1, textvariable=self.min)
        self.label_min.configure(font=("Arial", 12, 'bold'), anchor='s', fg=self.color3)

        self.numbers_of_oscillations = tk.StringVar(value="Количество колебаний: ")
        self.label_number_of_oscillations = tk.Label(self.root, bg=self.color1, textvariable=self.numbers_of_oscillations)
        self.label_number_of_oscillations.configure(font=("Arial", 12, 'bold'), anchor='w', fg=self.color3)


        # creating buttons to user can check self
        self.button_check = tk.Button(self.root, bg=self.color1, text="Проверить себя", fg=self.color3,
                                      command=self.check_self)
        self.button_check.configure(font=("Arial", 14, 'bold'), cursor='hand2')

        self.button_start = tk.Button(self.root, bg=self.color1, fg=self.color3,text="СТАРТ",
                                      command=lambda: self.start_oscillation())
        self.button_start.configure(font=("Arial", 14, 'bold'), cursor='hand2')
        self.button_start.place(relx=0.5, rely=0.5, relwidth=0.34, relheight=0.08, anchor="center")

        self.button_stop = tk.Button(self.root, bg=self.color1, text="Завершить", fg=self.color3,
                                     command=self.stop_oscillation)
        self.button_stop.configure(font=("Arial", 14, 'bold'), cursor='hand2')

        self.button_repeat1 = tk.Button(self.frame_win, command=self.repeat,
                                        relief='groove', cursor='hand2')
        self.button_repeat1.configure(bg=self.color2, highlightthickness=3,
                                      text='Заново', font=("Arial", 14))
        self.button_repeat1.place(relx=0.5, rely=0.9, anchor='center', relheight=0.1, relwidth=0.6)

        self.button_repeat2 = tk.Button(self.frame_over, command=self.repeat,
                                        relief='groove', cursor='hand2')
        self.button_repeat2.configure(bg=self.color2, highlightthickness=3,
                                      text='Заново', font=("Arial", 14))
        self.button_repeat2.place(relx=0.5, rely=0.9, anchor='center', relheight=0.1, relwidth=0.6)

        # entry for enter length
        self.entry = ttk.Entry(self.root)
        self.entry.configure(font=("Times New Roman", 14, 'bold'), foreground=self.color4)
        self.entry.insert(0, "Найдите длину (1-10 м)")

        #create frame of information
        self.frame_info = tk.Frame(self.root, bg=self.color1)
        self.frame_info.configure(highlightbackground=self.color2, highlightthickness=2, relief='groove')
        self.frame_info.place(relx=0, rely=0)

        self.label_info_title = tk.Label(self.frame_info, bg=self.color1, fg=self.color3)
        self.label_info_title.configure(text='Информация', font=("Arial black", 14, 'bold'), anchor='center')
        self.label_info_title.place(relx=0, rely=0, relwidth=1, relheight=0.12)

        self.label_info_text = tk.Label(self.frame_info, bg=self.color1, fg=self.color3)
        self.label_info_text.configure(font=("Arial", 16), anchor='n',
                                       text='   Данная программа написна для того,'
                                            '\nчтобы помочь в изучении математи-'
                                            '\nческого маятника. Запуская каждый'
                                            '\nраз игру, длина нити выбирается'
                                            '\nс помощью датчика случайных чисел.'
                                            '\nПользователь должен рассчитать длину нити.'
                                            '\nЕсли относительная неточность не превышает'
                                            '\n10 %, то ответ считается правильным.')
        self.label_info_text.place(relx=0, rely=0.12, relwidth=1, relheight=0.68)

        self.label_info_author = tk.Label(self.frame_info, bg=self.color1, fg=self.color3)
        self.label_info_author.configure(font=("Arial", 12, 'bold'), anchor='sw',
                                         text='Автор: Ильичев Роман', padx=10)
        self.label_info_author.place(relx=0, rely=0.8, relwidth=1, relheight=0.2)

        self.frm1.tag_raise(self.background)
        self.frm1.bind("<Button-1>", lambda event: self.root.focus_set())
        self.frm2.bind("<Button-1>", lambda event: self.root.focus_set())
        self.entry.bind("<FocusIn>", lambda event: self.entry.delete(0, 'end') if self.entry.get() == "Найдите длину (1-10 м)" else None)
        self.entry.bind("<FocusIn>", lambda event: self.entry.configure(foreground=self.color3), add="+")
        self.entry.bind("<FocusOut>", lambda event: self.entry.insert(0, "Найдите длину (1-10 м)") if self.entry.get() == "" else None)
        self.entry.bind("<FocusOut>", lambda event: self.entry.configure(foreground=self.color4) if self.entry.get() == "Найдите длину (1-10 м)" else None, add="+")

        self.label_question.bind('<Enter>', lambda event: self.frame_info.place(relx=0.5, rely=0.5,
                                                                                relwidth=0.7, relheight=0.6,
                                                                                anchor='center'))
        self.label_question.bind('<Leave>', lambda event: self.frame_info.place_forget())

        self.root.mainloop()


    def start_oscillation(self):
        self.meters = (randint(10, 100) / 10)
        k = 320 / self.meters
        self.length_thread = self.meters * k
        self.mass_pendulum = 10
        self.radius_ball = self.length_thread * 0.1
        self.angle_deflection = np.pi / 3
        self.g = 9.8
        self.acceleration = -self.g * np.sin(self.angle_deflection)
        self.Oscillation_period = 2 * np.pi * np.sqrt((self.length_thread / k) / self.g)
        self.Cyclic_frequency = np.sqrt(self.g / (self.length_thread / k))

        # Setting coordinates
        self.coordinates_center = [self.width_root / 2, self.height_root * 0.05]
        self.coordinates_ball = [self.length_thread * np.sin(self.angle_deflection)
                                 - self.radius_ball + self.coordinates_center[0],
                                 self.length_thread * np.cos(self.angle_deflection)
                                 - self.radius_ball + self.coordinates_center[1],
                                 self.length_thread * np.sin(self.angle_deflection)
                                 + self.radius_ball + self.coordinates_center[0],
                                 self.length_thread * np.cos(self.angle_deflection)
                                 + self.radius_ball + self.coordinates_center[1]]
        self.coordinates_equilibrium = [self.coordinates_center[0],
                                        self.coordinates_center[1] + self.length_thread]

        self.frm1.delete(self.thread)
        self.frm1.delete(self.ball)

        # Drawing thread
        self.thread = self.frm1.create_line([self.coordinates_center[0],
                                             self.coordinates_center[1],
                                             self.length_thread * np.sin(self.angle_deflection) +
                                             self.coordinates_center[0],
                                             self.length_thread * np.cos(self.angle_deflection) +
                                             self.coordinates_center[1]])

        # Drawing ball
        self.ball = self.frm1.create_oval(self.coordinates_ball, fill='purple')


        self.entry.place(relx=0.33, rely=0.72, relwidth=0.34, relheight=0.08)
        self.button_check.place(relx=0.33, rely=0.81, relwidth=0.34, relheight=0.08)
        self.button_stop.place(relx=0.33, rely=0.9, relwidth=0.34, relheight=0.08)
        self.label_number_of_oscillations.place(relx=0, rely=0.65, relwidth=0.3, relheight=0.05)
        self.label_ms.place(relx=0.98, rely=0.65, relwidth=0.02, relheight=0.05)
        self.label_comma.place(relx=0.975, rely=0.65, relwidth=0.005, relheight=0.05)
        self.label_sec.place(relx=0.95, rely=0.65, relwidth=0.025, relheight=0.05)
        self.label_colon.place(relx=0.945, rely=0.65, relwidth=0.005, relheight=0.05)
        self.label_min.place(relx=0.92, rely=0.65, relwidth=0.025, relheight=0.05)
        self.label_image.place_forget()
        self.button_start.place_forget()
        self.frm1.delete(self.background)
        self.frame_win.place_forget()
        self.frame_over.place_forget()
        self.entry.delete(0, 'end')
        self.root.focus_set()
        self.label_question.place(relx=0.899, rely=0.899, relheight=0.1, relwidth=0.1)


        self.move_pendulum()

        self.stopwatch_begin = time.perf_counter()
        self.ms.set(value='0')
        self.sec.set(value='00')
        self.min.set(value='00')
        self.numbers_of_oscillations.set(value="Количество колебаний: ")

        self.update_stopwatch()



    def update_stopwatch(self):
        self.stopwatch_end = time.perf_counter()
        delta_time = self.stopwatch_end - self.stopwatch_begin
        self.ms.set(value=str(int((delta_time % 1) // 0.1)))

        if len(str(int((delta_time // 1) % 60))) == 2:
            self.sec.set(value=str(int((delta_time // 1) % 60)))
        else:
            self.sec.set(value=('0' + str(int((delta_time // 1) % 60))))

        if len(str(int((delta_time // 1) // 60))) == 2:
            self.min.set(value=str(int(((delta_time // 1) // 60) % 60)))
        else:
            self.min.set(value=('0' + str(int(((delta_time // 1) // 60) % 60))))

        self.numbers_of_oscillations.set(value=("Количество колебаний: " + str(int(delta_time // self.Oscillation_period))))
        self.id_update_stopwatch = self.root.after(10, self.update_stopwatch)


    def stop_oscillation(self):

        self.background = self.frm1.create_image(375, int((600 * 0.7 / 2)), anchor='center', image=self.blur_image1)
        self.label_image.place(x=0,y=0, relheight=1, relwidth=1)
        self.button_start.place(relx=0.5, rely=0.5, relwidth=0.34, relheight=0.08, anchor="center")

        self.entry.place_forget()
        self.button_check.place_forget()
        self.button_stop.place_forget()
        self.label_number_of_oscillations.place_forget()
        self.label_ms.place_forget()
        self.label_comma.place_forget()
        self.label_sec.place_forget()
        self.label_colon.place_forget()
        self.label_min.place_forget()
        self.label_question.place_forget()

        self.root.after_cancel(self.id_update_stopwatch)
        self.root.after_cancel(self.id_move_pendulum)


    def check_self(self):
        get_value: float = None
        flag = False
        try:
            get_value = float(self.entry.get())
            flag = True
        except:
            mb.showinfo(title="Внимание", message="Некорректное значение")
        if flag is True:
            if 0 <= get_value:
                error = (abs(self.meters - get_value)/self.meters) * 100
                if error <= 10:
                    self.background = self.frm1.create_image(375, int((600 * 0.7 / 2)), anchor='center',
                                                             image=self.blur_image1)

                    self.label_image.place(x=0, y=0, relheight=1, relwidth=1)

                    self.entry.place_forget()
                    self.button_check.place_forget()
                    self.button_stop.place_forget()
                    self.label_number_of_oscillations.place_forget()
                    self.label_ms.place_forget()
                    self.label_comma.place_forget()
                    self.label_sec.place_forget()
                    self.label_colon.place_forget()
                    self.label_min.place_forget()

                    self.label_win_text.config(text="Поздравляю, вы правильно ввели"
                                                    "\nзначение длины!"
                                                    "\nT = {} с"
                                                    "\nL = {} м"
                                                    "\nВаш ответ: {} м"
                                                    "\nОтносительная погрешность: {}%".format("%.1f" % self.Oscillation_period,
                                                                                              self.meters, get_value,"%.1f" % error))

                    self.frame_win.place(relx=0.5, rely=0.5, relwidth=0.7, relheight=0.6, anchor='center')

                else:
                    self.background = self.frm1.create_image(375, int((600 * 0.7 / 2)), anchor='center',
                                                             image=self.blur_image1)

                    self.label_image.place(x=0, y=0, relheight=1, relwidth=1)

                    self.entry.place_forget()
                    self.button_check.place_forget()
                    self.button_stop.place_forget()
                    self.label_number_of_oscillations.place_forget()
                    self.label_ms.place_forget()
                    self.label_comma.place_forget()
                    self.label_sec.place_forget()
                    self.label_colon.place_forget()
                    self.label_min.place_forget()

                    self.label_over_text.config(text="Вы неправильно расчитали длину"
                                                     "\nпопробуйте ещё раз"
                                                     "\nT = {} с"
                                                     "\nL = {} м"
                                                     "\nВаш ответ: {} м"
                                                     "\nОтносительная погрешность: {}%".format("%.1f" % self.Oscillation_period,
                                                                                               self.meters, get_value, "%.1f" % error))

                    self.frame_over.place(relx=0.5, rely=0.5, relwidth=0.7, relheight=0.6, anchor='center')
            else:
                mb.showinfo(title="Внимание", message="Отрицательное значение")
    def repeat(self):
        self.start_oscillation()



    def move_pendulum(self):
        changed_angle = self.angle_deflection * np.cos(self.Cyclic_frequency * (self.stopwatch_end-self.stopwatch_begin))

        coordinates_ball_new = self.update_coordinates_ball(changed_angle)

        self.frm1.delete(self.thread)
        self.thread = self.frm1.create_line([self.coordinates_center[0],
                                             self.coordinates_center[1],
                                             coordinates_ball_new[0] + self.radius_ball,
                                             coordinates_ball_new[1] + self.radius_ball])

        self.frm1.tag_lower(self.thread)

        self.frm1.coords(self.ball, coordinates_ball_new)
        self.id_move_pendulum = self.root.after(10, self.move_pendulum)


    def update_coordinates_ball(self, angle):
         coordinates_ball_new = [self.length_thread * np.sin(angle)
                                 - self.radius_ball + self.coordinates_center[0],
                                 self.length_thread * np.cos(angle)
                                 - self.radius_ball + self.coordinates_center[1],
                                 self.length_thread * np.sin(angle)
                                 + self.radius_ball + self.coordinates_center[0],
                                 self.length_thread * np.cos(angle)
                                 + self.radius_ball + self.coordinates_center[1]]
         return coordinates_ball_new




if __name__ == "__main__":
    Pendulum()