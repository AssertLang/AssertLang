#include <string>
#include <map>

std::map<std::string,std::string> capabilities(){ return {{ {"tool", "custom-tool-template"}, {"versions", "v1"}, {"features", "validation,envelope,idempotency"} }}; }
std::map<std::string,std::string> ok(){ return {{ {"ok", "true"}, {"version", "v1"} }}; }
std::map<std::string,std::string> err(const std::string& code,const std::string& msg){ return {{ {"ok", "false"}, {"version", "v1"}, {"error", code+":"+msg} }}; }

std::map<std::string,std::string> handle(){ /* TODO validate/implement */ return ok(); }
