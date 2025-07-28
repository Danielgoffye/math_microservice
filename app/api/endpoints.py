
from fastapi import APIRouter, HTTPException, Depends, Request
from sqlalchemy.orm import Session
from app.services import math_service
from app.services.math_service import (
    _cached_fibonacci,
    _cached_factorial,
    _cached_pow
)
from app.schemas import operations
from app.db.deps import get_db
from app.models.request_log import RequestLog
import json
from sqlalchemy import func
from pathlib import Path


router = APIRouter()


@router.post("/pow", response_model=operations.PowerResponse)
def calculate_power(
    payload: operations.PowerRequest,
    db: Session = Depends(get_db)
):
    info_before = _cached_pow.cache_info()
    result = math_service.compute_pow(payload.base, payload.exponent)
    info_after = _cached_pow.cache_info()
    was_cached = int(info_before.hits < info_after.hits)

    db.add(
        RequestLog(
            operation="pow",
            parameters=json.dumps(payload.dict()),
            result=str(result),
            is_cached=was_cached,
            user_id=payload.user_id
        )
    )
    db.commit()
    return {"result": result}


@router.post("/factorial", response_model=operations.FactorialResponse)
def calculate_factorial(
    payload: operations.FactorialRequest,
    db: Session = Depends(get_db)
):
    try:
        info_before = _cached_factorial.cache_info()
        result = math_service.compute_factorial(payload.number)
        info_after = _cached_factorial.cache_info()
        was_cached = int(info_before.hits < info_after.hits)

        db.add(
            RequestLog(
                operation="factorial",
                parameters=json.dumps(payload.dict()),
                result=str(result),
                is_cached=was_cached,
                user_id=payload.user_id
            )
        )
        db.commit()
        return {"result": result}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/fibonacci", response_model=operations.FibonacciResponse)
def calculate_fibonacci(
    payload: operations.FibonacciRequest,
    db: Session = Depends(get_db)
):
    try:
        info_before = _cached_fibonacci.cache_info()
        result = math_service.compute_fibonacci(payload.n)
        info_after = _cached_fibonacci.cache_info()
        was_cached = int(info_before.hits < info_after.hits)

        db.add(
            RequestLog(
                operation="fibonacci",
                parameters=json.dumps(payload.dict()),
                result=str(result),
                is_cached=was_cached,
                user_id=payload.user_id
            )
        )
        db.commit()
        return {"result": result}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/history")
def get_history(request: Request, db: Session = Depends(get_db)):
    user_id = request.query_params.get("user_id")

    print("Received user_id:", user_id)  # Debugging statement

    if not user_id or not user_id.isdigit():
        raise HTTPException(
            status_code=400, detail="Invalid or missing User ID."
        )

    logs = db.query(RequestLog)\
             .filter(RequestLog.user_id == int(user_id))\
             .order_by(RequestLog.timestamp.desc())\
             .all()

    response = []
    for log in logs:
        response.append({
            "operation": log.operation,
            "parameters": log.parameters,
            "result": log.result,
            "timestamp": log.timestamp.strftime("%Y-%m-%d %H:%M"),
            "is_cached": log.is_cached
        })

    print("Logs found:", len(logs))
    print("user_id type:", type(user_id))
    return response


@router.get("/metrics")
def get_metrics(db: Session = Depends(get_db)):
    total = db.query(RequestLog).count()
    from_cache = db.query(RequestLog).filter(RequestLog.is_cached == 1).count()
    by_operation = db.query(RequestLog.operation, func.count())\
        .group_by(RequestLog.operation)\
        .all()

    operation_summary = {op: count for op, count in by_operation}

    metrics_path = Path("metrics.txt")
    metrics_path.write_text(
        json.dumps({
            "total_requests": total,
            "cache_hits": from_cache,
            "cache_hit_rate": (
                f"{(from_cache / total * 100):.2f}%" if total else "0%"
            ),
            "operations": operation_summary
        }, indent=2),
        encoding="utf-8"
    )

    return {
        "total_requests": total,
        "cache_hits": from_cache,
        "cache_hit_rate": (
            f"{(from_cache / total * 100):.2f}%" if total else "0%"
        ),
        "operations": operation_summary
    }
