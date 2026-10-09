#!/usr/bin/env python3
"""Tiny stdio MCP client for craft-studio servers. Usage: mcpc.py <app> <json-requests-file|->"""
import json, subprocess, sys, os
PLUGIN='/home/claude/plugin-src/craft-studio'
class Client:
    def __init__(self, app, cwd='/home/claude/craft'):
        env=dict(os.environ, CLAUDE_PLUGIN_ROOT=PLUGIN)
        self.p=subprocess.Popen(['python3',f'{PLUGIN}/bin/craft-mcp',app],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=sys.stderr,text=True,bufsize=1,cwd=cwd,env=env)
        self.n=0
        self.call_raw('initialize',{"protocolVersion":"2025-06-18","capabilities":{},"clientInfo":{"name":"claude","version":"1"}})
        self.p.stdin.write(json.dumps({"jsonrpc":"2.0","method":"notifications/initialized"})+"\n"); self.p.stdin.flush()
    def call_raw(self, method, params):
        self.n+=1; i=self.n
        self.p.stdin.write(json.dumps({"jsonrpc":"2.0","id":i,"method":method,"params":params})+"\n"); self.p.stdin.flush()
        while True:
            line=self.p.stdout.readline()
            if not line: raise RuntimeError('server closed')
            try: m=json.loads(line)
            except ValueError: continue
            if m.get('id')==i: return m
    def tools(self): return self.call_raw('tools/list',{})['result']['tools']
    def call(self, name, args):
        r=self.call_raw('tools/call',{"name":name,"arguments":args})
        if 'error' in r: return {'error':r['error']}
        return r['result']
