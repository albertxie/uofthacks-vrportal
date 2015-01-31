import myo
from myo.lowlevel import pose_t, stream_emg
from myo.six import print_
import random
import win32api, win32con

myo.init()

SHOW_OUTPUT_CHANCE = 0.01

class Stack(list):

    def __init__(self, M):
        self.maxSize = M
        self._data = []


    def add(self, element):

        if len(self._data) < self.maxSize:
            self._data.append(element)

        else:
            self._data = [self._data[x - 1] for x in range(len(self._data))]
            self._data[-1] = element


    def midpoint(self):
        if len(self._data) > 0:
            cache = self._data[::]
            cache.sort()
            return cache[len(cache) // 2]

        else:
            raise Exception("Stack must be populated to get midpoint.")


class Listener(myo.DeviceListener):

    orientation_yee = [0,0,0,0]

    global is_debug
    is_debug = True

    global middle
    middle = False

    def left_click(self):
        win32api.SetCursorPos((0,0))
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0,0,0)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0,0,0)
        if is_debug: print("Left Mouse Key Event")

    def right_click(self):
        win32api.SetCursorPos((0,0))
        win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN,0,0,0,0)
        win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP,0,0,0,0)
        if is_debug: print("Right Mouse Key Event")

    def middle_click(self):
        win32api.SetCursorPos((0,0))
        win32api.mouse_event(win32con.MOUSEEVENTF_MIDDLEDOWN,0,0,0,0)
        win32api.mouse_event(win32con.MOUSEEVENTF_MIDDLEUP,0,0,0,0)
        if is_debug: print("Middle Mouse Key Event")

    def on_connect(self, myo, timestamp):
        if is_debug: print_("Connected to Myo")

        myo.vibrate('short')
        myo.request_rssi()

    def on_rssi(self, myo, timestamp, rssi):
        if is_debug: print_("RSSI:", rssi)

    def on_event(self, event):
        r""" Called before any of the event callbacks. """

    def on_event_finished(self, event):
        r""" Called after the respective event callbacks have been
        invoked. This method is *always* triggered, even if one of
        the callbacks requested the stop of the Hub. """

    def on_pair(self, myo, timestamp):
        if is_debug:
            print_('Paired')
            print_("If you don't see any responses to your movements, try re-running the program or making sure the Myo works with Myo Connect (from Thalmic Labs).")
            #print_("Double tap enables EMG.")
            #print_("Spreading fingers disables EMG.\n")

    def on_disconnect(self, myo, timestamp):
        if is_debug: print_('on_disconnect')


    def on_pose(self, myo, timestamp, pose):
        if is_debug: print_('on_pose', pose)

        arm_boundary = -0.1
        global orientation_yee
        global middle

        if pose == pose_t.double_tap:
            if is_debug: print_("double_tap")
            #myo.set_stream_emg(stream_emg.enabled)

        elif pose == pose_t.fist:
            if is_debug: print_("fist")
            self.middle_click()

        elif(pose == pose_t.fingers_spread) and (orientation_yee[0] < arm_boundary):
            if middle == True:
                self.middle_click()
            print_("Left Click")
            self.left_click()

        elif(pose == pose_t.fingers_spread) and (orientation_yee[0] > arm_boundary):
            if middle == True:
                self.middle_click()
            print_("Right Click")
            self.right_click()

        elif pose == pose_t.wave_in:
            if middle == True:
                self.middle_click()


    def on_orientation_data(self, myo, timestamp, orientation):
        global orientation_yee
        orientation_yee = orientation
        show_output('orientation', orientation)

    def on_accelerometor_data(self, myo, timestamp, acceleration):
        if is_debug: show_output('acceleration', acceleration)

    def on_gyroscope_data(self, myo, timestamp, gyroscope):
        if is_debug: show_output('gyroscope', gyroscope)

    def on_unlock(self, myo, timestamp):
        if is_debug: print_('unlocked')

    def on_lock(self, myo, timestamp):
        if is_debug: print_('locked')

    def on_sync(self, myo, timestamp, arm, x_direction):
        if is_debug: print_('synced', arm, x_direction)

    def on_unsync(self, myo, timestamp):
        print_('unsynced')

    def on_emg(self, myo, timestamp, emg):
        if is_debug: show_output('emg', emg)


def show_output(message, data):
    if random.random() < SHOW_OUTPUT_CHANCE: 
        print_(message + ':' + str(data))


def main():
    hub = myo.Hub()
    hub.set_locking_policy(myo.locking_policy.none)
    hub.run(1000, Listener())

    # Listen to keyboard interrupts and stop the
    # hub in that case.
    try:
        while hub.running:
            myo.time.sleep(0.2)
    except KeyboardInterrupt:
        print_("Quitting ...")
        hub.stop(True)

if __name__ == '__main__':
    main()
