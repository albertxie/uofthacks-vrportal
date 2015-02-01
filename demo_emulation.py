import math
import myo
from myo.lowlevel import pose_t, stream_emg
from myo.six import print_
import random
import win32api, win32con

myo.init()

#DEMO CODE
class Listener(myo.DeviceListener):

    global is_debug
    is_debug = False

    global middle
    middle = False

    global euler_orientation

    #Threshold in which the Myo is considered to be "upside down"
    global arm_boundary
    arm_boundary = 40

    def left_click(self):
        ''' (Listener) -> NoneType
        Emulates a left mouse click in Windows at position (0, 0)
        '''
        win32api.SetCursorPos((0, 0))
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)

        if is_debug:
            print("Left Mouse Key Event")

    def right_click(self):
        ''' (Listener) -> NoneType
        Emulates a right mouse click in Windows at position (0, 0)
        '''
        win32api.SetCursorPos((0, 0))
        win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, 0, 0, 0, 0)
        win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, 0, 0, 0, 0)

        if is_debug:
            print("Right Mouse Key Event")

    def middle_click(self):
        ''' (Listener) -> NoneType
        Emulates a middle (wheel) mouse click in Windows at position (0, 0)
        '''
        win32api.SetCursorPos((0, 0))
        win32api.mouse_event(win32con.MOUSEEVENTF_MIDDLEDOWN, 0, 0, 0, 0)
        win32api.mouse_event(win32con.MOUSEEVENTF_MIDDLEUP, 0, 0, 0, 0)

        if is_debug:
            print("Middle Mouse Key Event")

    def on_connect(self, myo, timestamp):
        ''' (Listener, Myo, str) -> NoneType
        Vibrates the Myo band once a connection has been established
        '''
        if is_debug:
            print_("Connected to Myo")

        myo.vibrate('short')
        myo.request_rssi()

    def on_rssi(self, myo, timestamp, rssi):
        ''' (Listener, Myo, str, rssi) -> NoneType
        Displays RSSI state
        '''
        if is_debug:
            print_("RSSI:", rssi)

    def on_event(self, event):
        r""" Called before any of the event callbacks. """

    def on_event_finished(self, event):
        r""" Called after the respective event callbacks have been
        invoked. This method is *always* triggered, even if one of
        the callbacks requested the stop of the Hub. """

    def on_pair(self, myo, timestamp):
        ''' (Listener, Myo, str) -> NoneType
        Displays info when a connection has been established
        '''

        if is_debug:
            print_('Paired')
            print_("If you don't see any responses to your movements, try re-running the program or making sure the Myo works with Myo Connect (from Thalmic Labs).")

    def on_disconnect(self, myo, timestamp):
        ''' (Listener, Myo, str) -> NoneType
        Displays info when a connection is terminated
        '''

        if is_debug:
            print_('on_disconnect')


    def on_pose(self, myo, timestamp, pose):
        ''' (Listener, Myo, str) -> NoneType
        Triggers specific events when specific Myo positions are detected
        '''

        if is_debug:
            print_('on_pose', pose)

        global middle
        global euler_orientation

        if pose == pose_t.double_tap and is_debug:
            print_("double_tap")

        elif pose == pose_t.fist:
            if is_debug:
                print_("fist")

            self.middle_click()

        #When finger_spread is detected with palm facing down
        elif(pose == pose_t.fingers_spread) and (euler_orientation[0] <= arm_boundary):

            if middle == True:
                self.middle_click()

            if is_debug:
                print_("Left Click")

            self.left_click()

        #When finger_spread is detected with palm facing up
        elif(pose == pose_t.fingers_spread) and (euler_orientation[0] > arm_boundary):
            if middle == True:
                self.middle_click()

            if is_debug:
                print_("Right Click")

            self.right_click()


    def on_orientation_data(self, myo, timestamp, orientation):
        ''' (Listener, Myo, str, Quaternian) -> NoneType
        Translate current quaternian floats in to Euler numbers in radians
        '''

        global euler_orientation

        #Unpacking the quaternian representation to individual floats
        x, y, z, w = orientation


        #Translating quaternian data to euler numbers
        roll = math.atan(2*(w*x + y*z) / (1 - 2*(x**2 + y**2))) * (180/math.pi)
        pitch = math.asin(max(-1, min(1, 2*(w*y - x*z)))) * (180 / math.pi)
        yaw = math.atan(2*(w*z + x*y) / (1 - 2*(y**2 + z**2))) * (180 / math.pi)


        #Translating to radians and scaled accordingly
        scale = 5
        Roll = ((roll + math.pi) / (math.pi * 2)) * scale 
        Pitch = ((pitch + math.pi/2) / (math.pi)) * scale
        Yaw = ((yaw + math.pi) / (math.pi * 2))  * scale


        #Taking the absulote value of each value
        Roll = abs(round(Roll, 0))
        Pitch = abs(round(Pitch, 0))
        Yaw = abs(round(Yaw, 0))

        euler_orientation = [Roll, Pitch, Yaw]
        #print("Roll: {}, Pitch: {}, Yaw: {}".format(Roll, Pitch, Yaw))
        print("{:<60} | {:<60} | {:<60}\n".format("#"*int(Roll), "*"*int(Pitch), "="*int(Yaw)))
        


    #More debugging methods, print data on specific Myo triggers 

    def on_accelerometor_data(self, myo, timestamp, acceleration):
        if is_debug:
            show_output('acceleration', acceleration)

    def on_gyroscope_data(self, myo, timestamp, gyroscope):
        if is_debug:
            show_output('gyroscope', gyroscope)

    def on_unlock(self, myo, timestamp):
        if is_debug:
            print_('unlocked')

    def on_lock(self, myo, timestamp):
        if is_debug:
            print_('locked')

    def on_sync(self, myo, timestamp, arm, x_direction):
        if is_debug:
            print_('synced', arm, x_direction)

    def on_unsync(self, myo, timestamp):
        print_('unsynced')

    def on_emg(self, myo, timestamp, emg):
        if is_debug:
            show_output('emg', emg)


def show_output(message, data):
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
