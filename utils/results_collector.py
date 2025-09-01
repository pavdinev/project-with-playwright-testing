from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

@dataclass
class Step:
    name: str
    ok: bool
    details: Dict[str, Any] = field(default_factory=dict)

@dataclass
class UserResult:
    username: str
    steps: List[Step] = field(default_factory=list)
    timings: Dict[str, float] = field(default_factory=dict)
    login_time: Optional[float] = None
    screenshot: Optional[str] = None
    meta: Dict[str, Any] = field(default_factory=dict)

    def log(self, name: str, ok: bool, **details):
        self.steps.append(Step(name=name, ok=ok, details=details))
        return ok

    @property
    def errors(self) -> List[str]:
        return [s.name for s in self.steps if not s.ok]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "username": self.username,
            "steps": [{"name": s.name, "ok": s.ok, "details": s.details} for s in self.steps],
            "timings": self.timings,
            "login_time": self.login_time,
            "screenshot": self.screenshot,
            "meta": self.meta,
            "errors": self.errors,
        }
