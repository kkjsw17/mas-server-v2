<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://user-images.githubusercontent.com/39583312/232528373-ebed2da9-7046-4af4-bc45-81b0b4345aba.png">
    <source media="(prefers-color-scheme: light)" srcset="https://user-images.githubusercontent.com/39583312/232528362-7095f1fb-a3a2-4ffc-9396-e3e498f28a29.png">
    <img alt="Meeting Auto Summarization" src="https://user-images.githubusercontent.com/39583312/232528362-7095f1fb-a3a2-4ffc-9396-e3e498f28a29.png">
  </picture>
</p>

<p align="center">
  <h2 align="center">MAS: Meeting Auto Summarization</h2>
  <h3 align="center">Web Server v2 Repository</h3>
  <br />
  <br />
</p>

# Table of Contents
- [Introduction](#introduction)
- [Technologies](#technologies)
- [Features](#features)
  * [api server](#api-server)
  * [websocket server](#websocket-server)
  * [messaging server](#messaging-server)
  * [batch server (TODO)](#batch-server--todo-)
- [Docstring](#docstring)
  * [Format](#format)
  * [Example](#example)
  * [generated with ChatGPT](#generated-with-chatgpt)

<small><i><a href='http://ecotrust-canada.github.io/markdown-toc/'>Table of contents generated with markdown-toc 👍</a></i></small>

# Introduction
- **MAS**(**M**eeting **A**uto **S**ummarization)는 **자동 요약 기능이 포함된 화상회의 서비스**입니다.
- **STT**를 통해 실시간으로 기록된 회의 스크립트를 바탕으로 사용자가 지정한 보고서 형식에 맞춰 **회의 내용을 요약**하는 기술이 핵심입니다.
- 건국대학교 컴퓨터공학부 졸업 프로젝트의 일환으로 2021년 2학기부터 2022년 1학기까지 진행되었습니다.
- 해당 Repository는 MAS 웹 서버의 v2 버전입니다.
  - 기존 node.js 기반 구현체를 **python 환경**으로 마이그레이션합니다.
  - 대규모 리팩토링을 진행하여, 사실상 도메인만 동일한 새로운 프로젝트로 보아도 무방합니다.

# Technologies
- **Language**
  - python
- **Web Server Framework**
  - FastAPI
- **Database Management System**
  - MySQL
  - PostgreSQL (TODO)
- **Database Toolkit** (Python SQL toolkit and Object Relational Mapper)
  - SQLAlchemy
- **Data streaming**
  - Kafka
- **Batch Job Scheduling** (TODO)
  - airflow
- **Security**
  - OAuth2
    - Google
    - Kakao, Facebook, Naver, etc (TODO)
  - JWT
- **DevOps** (TODO)
  - AWS EKS
  - Github actions

# Features
## API server
- **User**
- **Script**
- **Meeting**
## Websocket server
- 회의실 별 실시간 스크립트 제공 채팅 서버 관리
- 스크립트 Producing to the message queue
## Messaging server
- 스크립트 Consuming 및 insert to DB
## Batch server (TODO)
- 매일 자정 삭제 후 30일이 지난 유저 delete from DB
- 매일 자정 삭제 후 24시간이 지난 스크립트 delete from DB
- 유저 일괄 메일 전송 기능

# Docstring
## Format
  - based on Google Style [[Link](https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html)]
## Example
```python
def function_with_pep484_type_annotations(param1: int, param2: str) -> bool:
    """
    Example function with PEP 484 type annotations.

    Args:
        param1 (int): The first parameter.
        param2 (str): The second parameter.

    Returns:
        bool: The return value. True for success, False otherwise.
    """
```
## generated with ChatGPT
- 모든 Docstring은 1차적으로 **ChatGPT**를 통해 생성합니다.
- 직접 검수한 후 수정 작업을 거쳐 코드에 Docstring 탑재합니다.
