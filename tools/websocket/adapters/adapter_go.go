package websocket

import (
	"encoding/json"
	"errors"
)

type Response struct { Ok bool `json:"ok"`; Version string `json:"version"`; Data map[string]any `json:"data"`; Error *RespError `json:"error,omitempty"` }
type RespError struct { Code string `json:"code"`; Message string `json:"message"`; Details map[string]any `json:"details,omitempty"` }

func capabilities() map[string]any { return map[string]any{"tool": "websocket", "versions": []string{"v1"}, "features": []string{"validation","envelope","idempotency"}} }

func ok(data map[string]any) Response { if data==nil { data = map[string]any{} }; return Response{Ok:true, Version:"v1", Data:data} }
func err(code, msg string, details map[string]any) Response { return Response{Ok:false, Version:"v1", Error:&RespError{Code:code, Message:msg, Details:details}} }

func validateRequest(req map[string]any) error { if req==nil { return errors.New("request must be an object") }; return nil }

func Handle(req map[string]any) Response { if e:=validateRequest(req); e!=nil { return err("E_SCHEMA", e.Error(), nil) }; /* TODO implement */ return ok(map[string]any{}) }
