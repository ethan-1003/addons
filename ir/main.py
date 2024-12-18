from ir_receiver import IRReceiver

def decode_ir_signal(signal_data, threshold_low=0.0004, threshold_high_0=0.0004, threshold_high_1=0.0015):
    """
    Giải mã tín hiệu IR thành chuỗi bit nhị phân dựa trên cặp LOW-HIGH.
    """
    bits = []
    for i in range(0, len(signal_data) - 1, 2):
        state_low, duration_low = signal_data[i]
        state_high, duration_high = signal_data[i + 1]

        if state_low == 0 and state_high == 1:
            if threshold_low <= duration_low <= threshold_low + 0.0003:
                if threshold_high_0 <= duration_high <= threshold_high_0 + 0.0003:
                    bits.append('0')
                elif threshold_high_1 <= duration_high <= threshold_high_1 + 0.0005:
                    bits.append('1')
    return ''.join(bits)

if __name__ == "__main__":
    # Khởi tạo IR Receiver
    ir = IRReceiver(chip_name="gpiochip0", line_offset=28)

    # Bắt tín hiệu IR
    signal = ir.capture_signal()

    # In tín hiệu ra màn hình
    ir.print_signal()

    # Giải mã tín hiệu IR
    decoded_bits = decode_ir_signal(signal)
    print("\nChuỗi nhị phân giải mã:")
    print(decoded_bits)

    # Lưu tín hiệu và kết quả giải mã ra file
    with open("ir_signal_data.txt", "w") as file:
        for state, time_length in signal:
            state_str = "LOW" if state == 0 else "HIGH"
            file.write(f"{state_str} trong {time_length:.6f} giây\n")
        file.write("\nChuỗi nhị phân giải mã:\n")
        file.write(decoded_bits)

    print("Tín hiệu và chuỗi giải mã đã được lưu vào file 'ir_signal_data.txt'.")
