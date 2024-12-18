import gpiod
import time

class IRReceiver:
    def __init__(self, chip_name="gpiochip0", line_offset=17):
        """
        Khởi tạo IR Receiver.
        :param chip_name: Tên chip GPIO (ví dụ: gpiochip0)
        :param line_offset: Offset của chân GPIO cần đọc tín hiệu.
        """
        self.chip_name = chip_name
        self.line_offset = line_offset
        self.signal_data = []  # Danh sách lưu tín hiệu HIGH/LOW và thời gian
        self.chip = None
        self.line = None

    def _setup_gpio(self):
        """Cấu hình chân GPIO để đọc tín hiệu IR."""
        self.chip = gpiod.Chip(self.chip_name)
        self.line = self.chip.get_line(self.line_offset)
        self.line.request(consumer="ir_sensor", type=gpiod.LINE_REQ_DIR_IN)

    def capture_signal(self):
        """
        Bắt tín hiệu IR từ cảm biến và lưu vào danh sách.
        :return: Danh sách [(trạng thái, thời gian giữ trạng thái)].
        """
        print("Đang ghi tín hiệu IR... Nhấn Ctrl+C để dừng.")
        self._setup_gpio()

        last_state = self.line.get_value()  # Trạng thái ban đầu
        last_change = time.time()  # Thời gian thay đổi trạng thái cuối cùng
        self.signal_data = []  # Reset dữ liệu cũ
        started = False  # Đánh dấu khi bắt đầu ghi nhận từ LOW

        try:
            while True:
                current_state = self.line.get_value()
                current_time = time.time()

                # Bỏ qua các tín hiệu HIGH ban đầu, chỉ bắt đầu từ LOW
                if not started:
                    if current_state == 0:  # Bắt đầu từ LOW
                        started = True
                        last_state = current_state
                        last_change = current_time
                    continue  # Bỏ qua HIGH ban đầu

                # Ghi nhận tín hiệu khi đã bắt đầu
                if current_state != last_state:
                    elapsed_time = current_time - last_change  # Thời gian giữ trạng thái
                    self.signal_data.append((last_state, elapsed_time))
                    last_state = current_state  # Cập nhật trạng thái
                    last_change = current_time

        except KeyboardInterrupt:
            print("Dừng ghi tín hiệu IR.")
        finally:
            self.line.release()
            return self.signal_data

    def print_signal(self):
        """In ra tín hiệu IR đã ghi nhận."""
        print("\nTín hiệu IR ghi nhận:")
        for state, time_length in self.signal_data:
            state_str = "LOW" if state == 0 else "HIGH"
            print(f"{state_str} trong {time_length:.6f} giây")

