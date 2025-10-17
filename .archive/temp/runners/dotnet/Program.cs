using System;
using System.IO;
using System.Linq;
using System.Collections.Generic;
using System.Net.Sockets;
using System.Text;
using System.Text.Json;
using System.Threading.Tasks;

namespace Runner;

internal class Program
{
  private record FileSpec(string path, string content, int mode);
  private record Request(string method, string task_id, FileSpec[] files, string? target_dir, string? cmd, string? cwd, int port, Dictionary<string,string>? env, string? log_path, int pid, string? host);

  private static void Ok(object data){ Console.WriteLine(JsonSerializer.Serialize(new{ ok=true, version="v1", data })); }
  private static void Err(string code,string message){ Console.WriteLine(JsonSerializer.Serialize(new{ ok=false, version="v1", error=new{ code, message } })); }

  public static int Main(string[] args)
  {
    string raw = "";
    for (var i=0;i<args.Length;i++) if (args[i]=="--json" && i+1<args.Length) raw=args[i+1];
    if (string.IsNullOrEmpty(raw)) raw = Console.In.ReadToEnd();
    var req = JsonSerializer.Deserialize<Request>(raw) ?? new("","",Array.Empty<FileSpec>(),null,null,null,0,null,null,0,null);

    switch(req.method){
      case "apply": {
        try{
          var target = req.target_dir ?? Path.Combine(".mcpd", req.task_id, "source");
          Directory.CreateDirectory(target);
          var writes=0;
          foreach(var f in req.files){
            var p = Path.Combine(target, f.path);
            Directory.CreateDirectory(Path.GetDirectoryName(p)!);
            File.WriteAllText(p, f.content ?? string.Empty, Encoding.UTF8);
            writes++;
          }
          Ok(new{ writes, target });
        } catch(Exception ex){ Err("E_FS", ex.Message); }
        return 0;
      }
      case "start": {
        try{
          var cwd = req.cwd ?? Directory.GetCurrentDirectory();
          var psi = new System.Diagnostics.ProcessStartInfo("bash","-lc \""+req.cmd+"\""){
            WorkingDirectory = cwd,
            RedirectStandardOutput = true,
            RedirectStandardError = true,
            UseShellExecute = false,
          };
          foreach(System.Collections.DictionaryEntry e in Environment.GetEnvironmentVariables()) psi.Environment[(string)e.Key]=(string)e.Value;
          psi.Environment["PORT"] = req.port.ToString();
          if (req.env!=null) foreach(var kv in req.env) psi.Environment[kv.Key]=kv.Value;
          var proc = System.Diagnostics.Process.Start(psi)!;
          if (!string.IsNullOrEmpty(req.log_path)){
            var logPath = req.log_path!;
            _ = Task.Run(async () => { try{ Directory.CreateDirectory(Path.GetDirectoryName(logPath)!); using var fs = new FileStream(logPath, FileMode.Append, FileAccess.Write, FileShare.ReadWrite); await proc.StandardOutput.BaseStream.CopyToAsync(fs);} catch { } });
            _ = Task.Run(async () => { try{ Directory.CreateDirectory(Path.GetDirectoryName(logPath)!); using var fs = new FileStream(logPath, FileMode.Append, FileAccess.Write, FileShare.ReadWrite); await proc.StandardError.BaseStream.CopyToAsync(fs);} catch { } });
          }
          Ok(new{ pid=proc.Id });
        } catch(Exception ex){ Err("E_RUNTIME", ex.Message);} return 0;
      }
      case "stop": {
        try{ var p = System.Diagnostics.Process.GetProcessById(req.pid); p.Kill(); Ok(new{ stopped=true }); } catch(Exception ex){ Err("E_RUNTIME", ex.Message);} return 0;
      }
      case "health": {
        try{ using var c = new TcpClient(); c.Connect(req.host??"127.0.0.1", req.port); Ok(new{ ready=true }); } catch { Ok(new{ ready=false }); } return 0;
      }
      default: Err("E_METHOD","unknown method"); return 1;
    }
  }
}

