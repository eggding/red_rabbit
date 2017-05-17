#!/bin/bash
protoc -I ./proto/ --python_out=./proto ./proto/login.proto
protoc -I ./proto/ --python_out=./proto ./proto/common_info.proto
protoc -I ./proto/ --python_out=./proto ./proto/create_room.proto
protoc -I ./proto/ --python_out=./proto ./proto/enter_room.proto
protoc -I ./proto/ --python_out=./proto ./proto/exit_room.proto
protoc -I ./proto/ --python_out=./proto ./proto/opt.proto
protoc -I ./proto/ --python_out=./proto ./proto/change_scene.proto
protoc -I ./proto/ --python_out=./proto ./proto/query_room_scene.proto
protoc -I ./proto/ --python_out=./proto ./proto/gm_config.proto
