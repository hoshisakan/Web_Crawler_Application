import traceback
import sys

class HandleException:
     @staticmethod
     def show_exp_detail_message(exp_object=None):
          error_class = exp_object.__class__.__name__
          # TODO 例外類型
          detail = exp_object.args[0]
          # TODO 引發例外原因
          cl, exc, tb = sys.exc_info()
          lastCallStack = traceback.extract_tb(tb)[-1]
          fileName = lastCallStack[0]
          lineNumber = lastCallStack[1]
          funcName = lastCallStack[2]
          errMsg = "File \"{}\", line {}, in {}: [{}] {}".format(
               fileName, lineNumber, funcName, error_class, detail)
          return errMsg