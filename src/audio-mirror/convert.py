import ffmpeg
import os

def convert_m4a_to_wav(input_path):
    if not os.path.exists(input_path):
        print(f"Error: The input file '{input_path}' does not exist.")
        return

    # Get the directory of the input file and create the output path
    output_path = os.path.join(os.path.dirname(input_path), "convert.wav")

    try:
        # Perform the conversion using ffmpeg
        ffmpeg.input(input_path).output(output_path, format='wav').run()
        print(f"Conversion complete: {output_path}")
    except ffmpeg.Error as e:
        print(f"FFmpeg error: {e.stderr.decode()}")
        raise

if __name__ == "__main__":
    input_path = input("Enter the path to the .m4a file: ")

    # Convert the file
    convert_m4a_to_wav(input_path)
