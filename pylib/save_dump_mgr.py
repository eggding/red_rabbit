# -*- coding: utf-8 -*-
# @Author  : jh.feng

import ffext
import traceback
import os, time, linecache
import tokenize, sys, inspect
import weakref, keyword, pydoc

class RecordVar(object):
    __UNDEF__ = []                          # a special sentinel object

    @classmethod
    def lookup(cls, name, frame, locals):
        """Find the value for a given name in the given environment."""
        if name in locals:
            return 'local', locals[name]
        if name in frame.f_globals:
            return 'global', frame.f_globals[name]
        if '__builtins__' in frame.f_globals:
            builtins = frame.f_globals['__builtins__']
            # if type(builtins) is type({}):
            if isinstance(builtins, dict):
                if name in builtins:
                    return 'builtin', builtins[name]
            else:
                if hasattr(builtins, name):
                    return 'builtin', getattr(builtins, name)
        return None, cls.__UNDEF__

    @classmethod
    def scanvars(cls, reader, frame, localvars):
        """Scan one logical line of Python and look up values of variables used."""
        cur_vars, lasttoken, parent, prefix, value = [], None, None, '', cls.__UNDEF__
        for ttype, token, start, end, line in tokenize.generate_tokens(reader):
            if ttype == tokenize.NEWLINE:
                break
            if ttype == tokenize.NAME and token not in keyword.kwlist:
                if lasttoken == '.':
                    if parent is not cls.__UNDEF__ and parent is not None:
                        if isinstance(parent, weakref.ProxyType) and bool(dir(parent)):
                            value = getattr(parent, token, cls.__UNDEF__)
                        else:
                            value = getattr(parent, token, cls.__UNDEF__)
                        cur_vars.append((prefix + token, prefix, value))
                else:
                    where, value = cls.lookup(token, frame, localvars)
                    cur_vars.append((token, where, value))
            elif token == '.':
                prefix += lasttoken + '.'
                parent = value
            else:
                parent, prefix = None, ''
            lasttoken = token
        return cur_vars

    @classmethod
    def recordvar(cls):
        etype, evalue, etb = sys.exc_info()
        records = inspect.getinnerframes(etb, 5)

        list_records = ["Detail:"]
        frame, sourcefile, lnum, func, lines, index = records[-1]
        sourcefile = sourcefile and os.path.abspath(sourcefile) or '?'
        args, varargs, varkw, var_locals = inspect.getargvalues(frame)
        call = ''
        if func != '?':
            call = 'in {0}{1}'.format(func, inspect.formatargvalues(args, varargs, varkw, var_locals,
                                                                    formatvalue=lambda objvalue: '={0}'.format(pydoc.text.repr(objvalue))))

        highlight = {}

        def reader(llnum=[lnum]):
            highlight[llnum[0]] = 1
            try:
                return linecache.getline(sourcefile, llnum[0])
            finally:
                llnum[0] += 1

        listvars = cls.scanvars(reader, frame, var_locals)

        rows = [' Current dump time: {}'.format(time.strftime("%Y-%m-%d %H:%M:%S")), ' {0} {1}'.format(sourcefile, call)]
        if index is not None:
            i = lnum - index
            for line in lines:
                num = '%6d ' % i
                rows.append(num + line.rstrip())
                i += 1

        rows.append(" Local Var:")

        done, dump = {}, []
        for k, v in frame.f_locals.iteritems():
            if not k.startswith('__'):
                dump.append("    {0} = {1}".format(k, pydoc.text.repr(v)))

                # if type(v) == InstanceType:
                #     pass
                # else:
                #     if type(v).__name__ == "GasPlayerEntity":
                #         dump.append("    playerid = {}".format(v.m_szID))
                #         dump.append("    name = {}".format(v.m_szName))

        for name, where, value in listvars:
            if name in done:
                continue
            if name in frame.f_locals:
                continue
            done[name] = 1
            if value is not cls.__UNDEF__:
                if where == 'global':
                    name = 'global ' + name
                elif where != 'local':
                    name = where + name.split('.')[-1]
                dump.append('    {0} = {1}'.format(name, pydoc.text.repr(value)))
            else:
                dump.append('    {0} undefined'.format(name))

        rows.append('\n'.join(dump))
        list_records.append('\n{0}\n'.format('\n'.join(rows)))
        return "".join(list_records)


def DumpTraceBack():
    szTrace = traceback.format_exc()
    try:
        szVar = RecordVar.recordvar()
    except:
        # 如果获取变量失败，则直接跳过
        szVar = ""

    szRet = szTrace + szVar
    # print(szRet)
    ffext.LOGERROR("FFSCENE_PYTHON", "{0}".format(szRet))
