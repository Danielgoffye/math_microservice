from fastapi import APIRouter, HTTPException, Depends
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session
from app.services import math_service
from app.schemas import operations
from app.db.deps import get_db
from app.models.request_log import RequestLog
import json
from sqlalchemy import func
from pathlib import Path


router = APIRouter()

# ------------------ /pow ------------------


@router.post("/pow", response_model=operations.PowerResponse)
def calculate_power(
    payload: operations.PowerRequest,
    db: Session = Depends(get_db),
    Authorize: AuthJWT = Depends()
):
    Authorize.jwt_required()
    user_id = int(Authorize.get_jwt_subject())

    result, was_cached = math_service.compute_pow(
        payload.base, payload.exponent
    )

    db.add(RequestLog(
        operation="pow",
        parameters=json.dumps(payload.dict()),
        result=str(result),
        is_cached=was_cached,
        user_id=user_id
    ))
    db.commit()
    return {"result": result}

# ------------------ /factorial ------------------


@router.post("/factorial", response_model=operations.FactorialResponse)
def calculate_factorial(
    payload: operations.FactorialRequest,
    db: Session = Depends(get_db),
    Authorize: AuthJWT = Depends()
):
    Authorize.jwt_required()
    user_id = int(Authorize.get_jwt_subject())

    try:
        result, was_cached = math_service.compute_factorial(payload.number)

        db.add(RequestLog(
            operation="factorial",
            parameters=json.dumps(payload.dict()),
            result=str(result),
            is_cached=was_cached,
            user_id=user_id
        ))
        db.commit()
        return {"result": result}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

# ------------------ /fibonacci ------------------


@router.post("/fibonacci", response_model=operations.FibonacciResponse)
def calculate_fibonacci(
    payload: operations.FibonacciRequest,
    db: Session = Depends(get_db),
    Authorize: AuthJWT = Depends()
):
    Authorize.jwt_required()
    user_id = int(Authorize.get_jwt_subject())

    try:
        result, was_cached = math_service.compute_fibonacci(payload.n)

        db.add(RequestLog(
            operation="fibonacci",
            parameters=json.dumps(payload.dict()),
            result=str(result),
            is_cached=was_cached,
            user_id=user_id
        ))
        db.commit()
        return {"result": result}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

# ------------------ /history ------------------


@router.get("/history")
def get_history(
    db: Session = Depends(get_db),
    Authorize: AuthJWT = Depends()
):
    Authorize.jwt_required()
    user_id = int(Authorize.get_jwt_subject())

    logs = db.query(RequestLog)\
             .filter(RequestLog.user_id == user_id)\
             .order_by(RequestLog.timestamp.desc())\
             .all()

    return [
        {
            "operation": log.operation,
            "parameters": log.parameters,
            "result": log.result,
            "timestamp": log.timestamp.strftime("%Y-%m-%d %H:%M"),
            "is_cached": log.is_cached
        }
        for log in logs
    ]

# ------------------ /metrics ------------------


@router.get("/metrics")
def get_metrics(
    db: Session = Depends(get_db),
    Authorize: AuthJWT = Depends()
):
    Authorize.jwt_required()

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
