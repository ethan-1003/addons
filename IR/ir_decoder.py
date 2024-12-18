def decode_ir_signal(signal_data, threshold_0=(0.0004, 0.0007), threshold_1=(0.0013, 0.0018)):
    """
    Giải mã tín hiệu IR thành chuỗi bit nhị phân dựa trên thời gian LOW.
    
    :param signal_data: Danh sách [(trạng thái, thời gian)] từ tín hiệu.
    :param threshold_0: Tuple ngưỡng thời gian cho bit '0' (min, max).
    :param threshold_1: Tuple ngưỡng thời gian cho bit '1' (min, max).
    :return: Chuỗi nhị phân giải mã.
    """
    bits = []  # Danh sách chứa các bit giải mã

    # Lặp qua tín hiệu và chỉ lấy LOW để giải mã
    for i in range(1, len(signal_data), 2):  # Bỏ qua trạng thái HIGH, chỉ xét LOW
        state, duration = signal_data[i]  # Lấy trạng thái và thời gian

        if state == 0:  # Chỉ xét LOW
            if threshold_0[0] <= duration <= threshold_0[1]:  # Ngưỡng cho bit '0'
                bits.append('0')
            elif threshold_1[0] <= duration <= threshold_1[1]:  # Ngưỡng cho bit '1'
                bits.append('1')

    return ''.join(bits)  # Trả về chuỗi bit nhị phân


def read_signal_from_file(file_path):
    """
    Đọc dữ liệu tín hiệu từ file văn bản.
    :param file_path: Đường dẫn file tín hiệu.
    :return: Danh sách [(trạng thái, thời gian)].
    """
    signal_data = []
    with open(file_path, 'r') as f:
        for line in f:
            if "LOW" in line:
                state = 0
            elif "HIGH" in line:
                state = 1
            else:
                continue

            # Trích thời gian từ dòng văn bản
            time_part = line.split("trong")[1].strip().split(" ")[0]
            time_length = float(time_part)
            signal_data.append((state, time_length))
    return signal_data


if __name__ == "__main__":
    # Đường dẫn đến file tín hiệu đã lưu
    file_path = "ir_signal_data.txt"  # File chứa tín hiệu từ IRReceiver

    try:
        # Đọc tín hiệu từ file
        signal_data = read_signal_from_file(file_path)
        print("Đọc dữ liệu tín hiệu thành công!")

        # Giải mã tín hiệu
        decoded_bits = decode_ir_signal(signal_data)
        print("\nChuỗi nhị phân giải mã:")
        print(decoded_bits)

    except FileNotFoundError:
        print(f"Lỗi: Không tìm thấy file '{file_path}'.")
    except Exception as e:
        print(f"Lỗi: {e}")

