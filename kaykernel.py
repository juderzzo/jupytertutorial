from shakti import k

from ipykernel.kernelbase import Kernel



from pexpect import replwrap, EOF

import pexpect



from subprocess import check_output

import os.path



import re

import signal

keywords = ["count"]

class kaykernel(Kernel):
    implementation = "k output"
    implementation_version = "1.0"
    language = "k"  # will be used for syntax highlighting
    language_version = "3.6"
    language_info = {
        "name": "k output",
        "mimetype": "text/plain",
        "file_extension": ".txt",
    }
    banner = "Perform K commands"
    def do_execute(
        self, code, silent, store_history=True, user_expressions=None, allow_stdin=False

    ):
        exitcode = False
        b = ""
        try:
            b = k(code.strip())
        except:
            if code == "exit()":
                print("exiting...")
                exitcode = True
            else:
                print("bad code")
        if not silent:
            stream_content = {"name": "stdout", "text": str(b)}
            self.send_response(self.iopub_socket, "stream", stream_content)
            # ok now we gotta prepare our data
            content = {
                "source": "kernel",
                "data": {"output": code},  # str(k(code)) + code},
            }
            self.send_response(self.iopub_socket, "display_data", content)
            # now return the dictionary with all the data for the client
            #try:
                #exitcde = int(self.bashwrapper.run_command('echo $?').rstrip())
            #except Exception:
                #exitcode = 1

            if exitcode:
                error_content = {'execution_count': self.execution_count,
                                'ename': '', 'evalue': str(exitcode), 'traceback': []}
                self.send_response(self.iopub_socket, 'error', error_content)
                error_content['status'] = 'error'
                return error_content
            else:
                return {
                    "status": "ok",
                    "execution_count": self.execution_count,
                    "payload": [],
                    "user_expressions": {},
                    }
        def do_complete(self, code, cursor_pos):
            space_idxs = [i for i, l in enumerate(code) if l == ' ']
            low_idxs = [s for s in space_idxs if s < cursor_pos]
            if low_idxs:
                low_cp = max([s for s in space_idxs if s < cursor_pos]) + 1
                key_start = code[low_cp:cursor_pos]
            else:
                low_cp = 0
                key_start = code[:cursor_pos]

                matches = [k for k in self.keywords if k.startswith(key_start)]
                content = {'matches' : matches, 'cursor_start' : low_cp,
                       'cursor_end' : cursor_pos, 'metadata' : {}, 'status' : 'ok'}
            return content



from ipykernel.kernelapp import IPKernelApp
IPKernelApp.launch_instance(kernel_class=kaykernel)
