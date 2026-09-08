import os

# Paths (make sure these match where your files are)
tflite_path = 'model/miner_model.tflite'
c_header_path = 'esp32_code/model_data.h'

# Read the TFLite model
with open(tflite_path, 'rb') as f:
    tflite_model = f.read()

# Convert to C array format
hex_lines = []
for i in range(0, len(tflite_model), 12):
    chunk = tflite_model[i:i + 12]
    hex_lines.append("  " + ", ".join([f"0x{b:02x}" for b in chunk]))

# Move the join logic outside the f-string to fix the error
hex_array_string = ",\n".join(hex_lines)

c_code = f"""#ifndef MODEL_DATA_H
#define MODEL_DATA_H

// Auto-generated from miner_model.tflite
const unsigned int g_model_len = {len(tflite_model)};
const unsigned char g_model[] = {{
{hex_array_string}
}};

#endif // MODEL_DATA_H
"""

# Save as model_data.h
os.makedirs(os.path.dirname(c_header_path), exist_ok=True)
with open(c_header_path, 'w') as f:
    f.write(c_code)

print(f"Success! Model array saved to {c_header_path}")