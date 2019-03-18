from tuning import Tuning
import pyaudio
# import usb.core, usb.util
import os, sys
import logging
import time, datetime
import wave
import collections
import webrtcvad
import audioop
import contextlib

import displayapp2

# Logger method
# =============================================================================

def create_logger():
    DATE = datetime.datetime.now()  # obtain today's date
    LOG_DIRECTORY = 'Logs'
    LOG_FILE = 'Logs/mic_log.log'

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)  # set the level of the newly created logger
    string_formatter = logging.Formatter('%(message)s')  # creates a message formatter

    if not os.path.exists(LOG_DIRECTORY):  # creating a directory to store log files if it does not exists
        os.makedirs(LOG_DIRECTORY)

    file_handler = logging.FileHandler(
        LOG_FILE)  # creates a file handler object which can direct logging output to a  log file
    stream_handler = logging.StreamHandler(
        sys.stderr)  # sends logging output to sys.stderr (default behaviour). so we have to  specifically state and direct it  to std.out

    file_handler.setFormatter(string_formatter)  # set the display format of the file handler
    stream_handler.setFormatter(string_formatter)  # set the display format of the file handler

    logger.addHandler(file_handler)  # add file handler to the created log file
    logger.addHandler(stream_handler)
    logger.info("\n\n================================= {} ======================================\n".format(
        DATE.strftime("%y-%m-%d %H:%M:%S")))

    return logger


# recording audio clips
# ============================================================================

class Recorder():
    def __init__(self, Mic_tuner, logger):

        self.RATE = 16000
        self.CHANNELS = 1
        self.FORMAT = pyaudio.paInt16
        self.CHUNK = 160
        self.WINDOW_SIZE = 30

        self.VAD = webrtcvad.Vad(3)
        self.RECORD_SECONDS = 1
        self.pyaudio_instance = pyaudio.PyAudio()
        self.logger = logger
        self.Mic_tuner = Mic_tuner
        self.file_name_list = []
        self.STARTING_THRESHOLD = 500  #900
        self.AVERAGE_THRESHOLD = 600   #1400

    # set parameter value
    # ========================================================================

    def set_parameter(self, param_name, param_value):
        self.Mic_tuner.write(param_name, param_value)

    # get parameter value
    # ========================================================================

    def get_parameter(self, param_name):
        while True:
            try:
                print self.Mic_tuner.read(param_name)
                time.sleep(0.01)
            except KeyboardInterrupt:
                break

    # showing the parameter values of  the  device
    # ========================================================================

    def show_device_current_status(self):
        self.Mic_tuner.read_all_current_values(self.Mic_tuner)

    #
    # ========================================================================

    def show_DOA(self):
        while True:
            try:
                print(self.Mic_tuner.direction)
                time.sleep(0.01)
            except KeyboardInterrupt:
                break

    # Detecting voice activity  in the environment
    # ========================================================================

    def is_voice_activity_detected(self):
        # flag = self.Mic_tuner.is_voice()
        # self.logger.info("VAD status : {}".format(flag))
        # return flag

        while True:
            try:
                print(self.Mic_tuner.is_voice())
                time.sleep(0.01)
            except KeyboardInterrupt:
                break

    # detecting speech in  the environment
    # =======================================================================

    def is_speech_detected(self):
        while True:
            try:
                print self.Mic_tuner.is_speech()
                time.sleep(0.01)
            except KeyboardInterrupt:
                break

    # obtain the  device index to usse in the latter stages
    # =======================================================================

    def get_device_index(self):

        for i in range(self.pyaudio_instance.get_device_count()):
            dev = self.pyaudio_instance.get_device_info_by_index(i)
            name = dev['name'].encode('utf-8')
            print dev
            if name.find('ReSpeaker 4 Mic Array (UAC1.0): USB Audio (hw:2,0)') >= 0 and dev[
                'maxInputChannels'] == self.CHANNELS:
                self.logger.info('{} with {} input channel/s is selected (index no: {}).'.format(dev['name'], dev[
                    'maxInputChannels'], i))
                self.INDEX = i
                break

    # set the audio stream  after obtaining the device index
    # ======================================================================

    def set_stream(self):
        self.logger.info('Setting the audio stream')
        self.stream = self.pyaudio_instance.open(
            # this will start storing audio data in its buffer as soon as this line is executed
            rate=self.RATE,
            format=self.FORMAT,  # sets the sample width in bytes
            channels=self.CHANNELS,
            input=True)

    # frames_per_buffer= self.CHUNK,
    # input_device_index=self.INDEX)

    # record 5 second long audio files
    # =======================================================================

    def record_audio_clips(self):

        ring_buffer2 = collections.deque(maxlen=(20))
        ring_buffer = collections.deque(maxlen=self.WINDOW_SIZE)
        voiced_frames = []
        rms_frames = []
        audio_clip_counter = 0
        self.set_stream()

        counter = 0
        rms_sum = 0
        rms_sum2 = 0
        start_time = 0
        start_silence_timer = 0

        calc_avg_flag = True

        spike_detected = False
        triggered = False
        buff_off = False

        try:

            while True:

                frame = self.stream.read(
                    self.CHUNK)  # this will block untill the specified amount of frames are red (from the buffer)

                is_speech = self.VAD.is_speech(frame, self.RATE)
                is_speech = 1 if is_speech else 0

                rms = audioop.rms(frame, 2)
                print "VAD : {} , RMS : {}".format(is_speech, rms)

                if displayapp2.flag1 == 0:
                    break

                if not buff_off:
                    ring_buffer2.append((frame, is_speech, rms))

                if counter < 18 and calc_avg_flag == True:
                    # ring_buffer.append((frame, is_speech))
                    rms_sum += rms
                    counter += 1
                elif calc_avg_flag == True:
                    # ring_buffer.append((frame, is_speech))
                    print counter
                    rms_avg = rms_sum / counter
                    print rms_avg
                    rms_sum = 0
                    counter = 0
                    calc_avg_flag = False
                    start_silence_timer = time.time()

                # if rms_avg < 500:
                # 	rms_avg = 500
                # elif 500 <= rms_avg < 1500:
                # 	pass
                # else:
                # 	calc_avg_flag = True

                elif calc_avg_flag == False:
                    if (rms >= self.STARTING_THRESHOLD and is_speech == 1) or spike_detected == True:

                        if not buff_off:
                            print ("fsfffew")
                            for f in ring_buffer2:
                                ring_buffer.append(f)
                            ring_buffer2.clear()
                            buff_off = True
                            spike_detected = True

                        else:
                            if not triggered:
                                if (time.time() - start_silence_timer) > 5:
                                    self.logger.info("Recalculating the average")
                                    spike_detected = False
                                    calc_avg_flag = True
                                    buff_off = False
                                    ring_buffer.clear()

                                ring_buffer.append((frame, is_speech, rms))
                                num_voiced = len([f for f, speech, rms in ring_buffer if speech])
                                if num_voiced > 26:  # 0.9 * ring_buffer.maxlen:
                                    start_time = time.time()
                                    print num_voiced, ring_buffer.maxlen
                                    audio_clip_counter += 1
                                    self.logger.info("Audio clip recording started {}".format(audio_clip_counter))
                                    triggered = True

                                    for f, s, r in ring_buffer:
                                        voiced_frames.append(f)
                                        rms_frames.append(r)
                            else:

                                voiced_frames.append(frame)
                                rms_frames.append(rms)
                                ring_buffer.append((frame, is_speech, rms))
                                num_unvoiced = len([f for f, speech, r in ring_buffer if not speech])

                                end_time = time.time()
                                if (end_time - start_time) > 4.73 or num_unvoiced > 26:  # 0.5* ring_buffer.maxlen:
                                    spike_detected = False
                                    calc_avg_flag = True
                                    start_time = 0
                                    triggered = False
                                    buff_off = False

                                    print num_unvoiced
                                    self.logger.info("Audio clip recording ended {}".format(audio_clip_counter))
                                    # voiced_frames  = b''.join(voiced_frames)
                                    # audio = sr.AudioData(voiced_frames, self.RATE, self.pyaudio_instance.get_sample_size(self.FORMAT))
                                    # self.recognize_audio(audio)
                                    # self.save_audio(voiced_frames)
                                    audio_length = len(rms_frames)
                                    for r in rms_frames:
                                        rms_sum2 += r

                                    a = rms_sum2 / audio_length
                                    print a
                                    if a > self.AVERAGE_THRESHOLD:
                                        print 'done....'
                                        voiced_frames = b''.join(voiced_frames)
                                        self.save_audio(voiced_frames)
                                        file_name = self.save_audio_as_raw(voiced_frames)
                                        return file_name

                                    ring_buffer.clear()
                                    voiced_frames = []
                                    rms_frames = []
                                    rms_sum2 = 0
                                    rms_sum = 0

                    elif spike_detected == False:
                        if (time.time() - start_silence_timer) > 5:
                            self.logger.info("Recalculating the average")
                            calc_avg_flag = True

        except KeyboardInterrupt:
            self.logger.info("Audio stream is closed  by KeyboardInterrupt")
        finally:  # this part gets executed whether an exception occurs or not
            self.logger.info("Last Audio clip recording ended {}".format(audio_clip_counter))
            if triggered == True:
                voiced_frames = b''.join(voiced_frames)
                self.save_audio_as_raw(voiced_frames)
                self.save_audio(voiced_frames)
            self.stream.close()
            self.pyaudio_instance.terminate()  # close pyaudio session

    # save recorded audio files as .wav files
    # =======================================================================

    def save_audio(self, audio_clip):
        date = datetime.datetime.now()
        file_name = 'records/{}/{}.wav'.format(date.strftime("%y-%m-%d"), date.strftime("%H-%M-%S"))
        file_directory = 'records/{}'.format(date.strftime("%y-%m-%d"))

        if not os.path.exists(file_directory):  # creating a directory to store audio files if it does not exists
            self.logger.info("Creating a directory for  the new day....")
            os.makedirs(file_directory)

        wf = wave.open(file_name, 'wb')
        wf.setnchannels(self.CHANNELS)
        wf.setsampwidth(self.pyaudio_instance.get_sample_size(self.FORMAT))
        wf.setframerate(self.RATE)
        wf.writeframes(audio_clip)
        wf.close()

    # save audio clips as raw file
    # ========================================================================

    def save_audio_as_raw(self, audio_clip):
        date = datetime.datetime.now()
        file_name = 'records/raw_audio_files/{}/{}.raw'.format(date.strftime("%y-%m-%d"), date.strftime("%H-%M-%S"))
        file_directory = 'records/raw_audio_files/{}'.format(date.strftime("%y-%m-%d"))
        return_file_name = '{}.raw'.format(date.strftime("%H-%M-%S"))
        return_list = [file_directory, return_file_name]

        if not os.path.exists(file_directory):  # creating a directory to store audio files if it does not exists
            self.logger.info("Creating a directory for  the new day....")
            os.makedirs(file_directory)

        raw_file = open(file_name, 'wb')
        raw_file.write(audio_clip)
        raw_file.close()

        return return_list

    # read .wav files
    # ========================================================================

    def read_wave(self, path):
        date = datetime.datetime.now()
        full_path = 'records/{}/{}'.format(date.strftime("%y-%m-%d"), path)
        with contextlib.closing(wave.open(full_path, 'rb')) as wf:
            num_channels = wf.getnchannels()
            assert num_channels == 1
            sample_width = wf.getsampwidth()
            assert sample_width == 2
            sample_rate = wf.getframerate()
            assert sample_rate in (8000, 16000, 32000, 48000)
            pcm_data = wf.readframes(wf.getnframes())
        return pcm_data, sample_rate


# Main method
# ============================================================================

def main(logger, read_audio=False):
    # device = usb.core.find(idVendor=0x2886, idProduct=0x0018)

    if True:
        logger.info('Device is connected...')
        # Mic_tuner = Tuning(device)
        recorder = Recorder(False, logger)
        # recorder.get_device_index()

        # recorder.set_parameter('GAMMA_E', 2.5)
        # recorder.set_parameter('GAMMA_ENL', 2.5)
        # recorder.set_parameter('GAMMA_ETAIL', 2.5)
        # recorder.set_parameter('NLATTENONOFF',1)

        # recorder.set_parameter('GAMMA_NN', 3)
        # recorder.set_parameter('GAMMA_NN_SR', 3)
        # recorder.set_parameter('GAMMA_NS', 3)
        # recorder.set_parameter('GAMMA_NS_SR', 3)

        # recorder.set_parameter('MIN_NN', 0.05)
        # recorder.set_parameter('MIN_NN_SR', 0.05)
        # recorder.set_parameter('MIN_NS', 0.05)
        # recorder.set_parameter('MIN_NS_SR', 0.05)

        # recorder.set_parameter('AGCDESIREDLEVEL', 0.01) #overall gain of the  audio increases
        # recorder.set_parameter('AGCMAXGAIN', 70)
        # recorder.set_parameter('AGCTIME', 0.2)
        # recorder.get_parameter('AECSILENCEMODE')

        # recorder.show_device_current_status()
        return recorder.record_audio_clips()
    #
    # else:
    #     logger.info('Device is disconnected... ')
    #     pass


# This deosnt run if the code is imported
# =============================================================================


#if __name__ == "__main__":
def auto_run():

    logger = create_logger()  # logger instance is created
    logger.info("Starting the process....\n")
    return_list = main(logger, read_audio=False)
    print return_list
    logger.info("\nEnding the process....")
    logger.info("\n\n================================ END ======================================\n")
    return return_list

# ==============================================================================
