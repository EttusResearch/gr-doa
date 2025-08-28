import numpy as np
from gnuradio import gr
from datetime import datetime
import os

class blk(gr.sync_block):
    """Triggered Float Recorder with Sample Skipping"""

    def __init__(self, skip_interval=20, samples_to_record=10):
        gr.sync_block.__init__(
            self,
            name='MUSIC_calibrated',
            in_sig=[np.float32],
            out_sig=[]
        )

        self.angle = 0
        self.folder = "testdata/calibrated/MUSIC"
        os.makedirs(self.folder, exist_ok=True)

        self.recording = False
        self.skip_interval = skip_interval
        self.samples_to_record = samples_to_record
        self.recorded_samples = []
        self.sample_counter = 0

        # Message-Port für Trigger
        self.message_port_register_in(gr.pmt.intern("in"))
        self.set_msg_handler(gr.pmt.intern("in"), self.handle_trigger)

    def handle_trigger(self, msg):
        if not self.recording and self.angle <= 180:
            print(f"[Trigger] Recording started at angle {self.angle}°")
            self.recording = True
            self.recorded_samples = []
            self.sample_counter = 0

    def work(self, input_items, output_items):
        in0 = input_items[0]

        for sample in in0:
            if self.recording:
                # Only record every skip_interval-th sample using modulo
                if self.sample_counter % self.skip_interval == 0:
                    self.recorded_samples.append(sample)

                self.sample_counter += 1

                if len(self.recorded_samples) >= self.samples_to_record:
                    # Save
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    filename = f"record_{self.angle}deg_{timestamp}.dat"
                    filepath = os.path.join(self.folder, filename)

                    with open(filepath, "w") as f:
                        for s in self.recorded_samples:
                            f.write(f"{s}\n")

                    print(f"[Recorder] File saved: {filepath}")

                    # reset recording
                    self.recording = False
                    self.angle += 10

                    if self.angle > 180:
                        print("[Recorder] Maximum angle limit reached. Recording stopped.")
                    break  # recording finished

        return len(in0)
