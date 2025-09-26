package main

import (
	"bufio"
	"encoding/json"
	"flag"
	"fmt"
	"net"
	"os"
	"os/exec"
	"path/filepath"
)

type FileSpec struct {
	Path    string `json:"path"`
	Content string `json:"content"`
	Mode    int    `json:"mode"`
}
type Request struct {
	Method    string            `json:"method"`
	TaskID    string            `json:"task_id"`
	Files     []FileSpec        `json:"files"`
	TargetDir string            `json:"target_dir"`
	Cmd       string            `json:"cmd"`
	Cwd       string            `json:"cwd"`
	Port      int               `json:"port"`
	Env       map[string]string `json:"env"`
	LogPath   string            `json:"log_path"`
	PID       int               `json:"pid"`
	Host      string            `json:"host"`
}

func outOk(data any) {
	b, _ := json.Marshal(map[string]any{"ok": true, "version": "v1", "data": data})
	fmt.Println(string(b))
}
func outErr(code, msg string) {
	b, _ := json.Marshal(map[string]any{"ok": false, "version": "v1", "error": map[string]string{"code": code, "message": msg}})
	fmt.Println(string(b))
}

func main() {
	jsonArg := flag.String("json", "", "json request")
	flag.Parse()
	var req Request
	if *jsonArg != "" {
		_ = json.Unmarshal([]byte(*jsonArg), &req)
	} else {
		_ = json.NewDecoder(os.Stdin).Decode(&req)
	}

	switch req.Method {
	case "apply":
		target := req.TargetDir
		if target == "" {
			target = "."
		}
		writes := 0
		for _, f := range req.Files {
			p := filepath.Join(target, f.Path)
			_ = os.MkdirAll(filepath.Dir(p), 0o755)
			_ = os.WriteFile(p, []byte(f.Content), 0o644)
			writes++
		}
		outOk(map[string]any{"writes": writes, "target": target})
	case "start":
		env := os.Environ()
		env = append(env, fmt.Sprintf("PORT=%d", req.Port))
		for k, v := range req.Env {
			env = append(env, fmt.Sprintf("%s=%s", k, v))
		}
		if req.Cwd == "" {
			req.Cwd = "."
		}
		cmd := exec.Command("bash", "-lc", req.Cmd)
		cmd.Dir = req.Cwd
		cmd.Env = env
		stdout, _ := cmd.StdoutPipe()
		stderr, _ := cmd.StderrPipe()
		if err := cmd.Start(); err != nil {
			outErr("E_RUNTIME", err.Error())
			return
		}
		if req.LogPath != "" {
			go func() {
				f, _ := os.OpenFile(req.LogPath, os.O_CREATE|os.O_WRONLY|os.O_APPEND, 0o644)
				defer f.Close()
				r := bufio.NewReader(stdout)
				for {
					b, _, e := r.ReadLine()
					if e != nil {
						break
					}
					f.Write(append(b, '\n'))
				}
			}()
			go func() {
				f, _ := os.OpenFile(req.LogPath, os.O_CREATE|os.O_WRONLY|os.O_APPEND, 0o644)
				defer f.Close()
				r := bufio.NewReader(stderr)
				for {
					b, _, e := r.ReadLine()
					if e != nil {
						break
					}
					f.Write(append(b, '\n'))
				}
			}()
		}
		outOk(map[string]any{"pid": cmd.Process.Pid})
	case "stop":
		p, _ := os.FindProcess(req.PID)
		_ = p.Kill()
		outOk(map[string]any{"stopped": true})
	case "health":
		h := req.Host
		if h == "" {
			h = "127.0.0.1"
		}
		c, e := net.Dial("tcp", fmt.Sprintf("%s:%d", h, req.Port))
		if e == nil {
			_ = c.Close()
			outOk(map[string]any{"ready": true})
		} else {
			outOk(map[string]any{"ready": false})
		}
	default:
		outErr("E_METHOD", "unknown method")
	}
}
