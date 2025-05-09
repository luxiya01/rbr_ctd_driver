import rclpy
from std_msgs.msg import String
from rbr_ctd_interfaces.msg import Topics
import serial
import time

def main():
    port = '/dev/ttyUSB1'
    baudrate = 115200

    rclpy.init()
    node = rclpy.create_node('serial_reader_ctd')
    rate = node.create_rate(10)  # 10 Hz
    
    # Create a publisher to publish the data
    publisher = node.create_publisher(String, Topics.CTD_RAW_TOPIC, 10)
    
    # Open the serial port
    connected = False
    while not connected and rclpy.ok():
        try:
            ser = serial.Serial(port, baudrate, timeout=1)
            connected = True
        except serial.SerialException as e:
            node.get_logger().error(f"Error opening serial port: {e}")
            rate.sleep()
    
    while rclpy.ok() and connected:
        line = ser.readline().decode('utf-8').strip()
        if len(line) > 0:
            # Create a String message and publish it
            msg = String()
            msg.data = line
            publisher.publish(msg)
            node.get_logger().info(f'Publishing: {msg.data}')
            rate.sleep()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
    finally:
        rclpy.shutdown()