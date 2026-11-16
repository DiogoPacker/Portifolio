from pydantic import BaseModel, ConfigDict, HttpUrl


class PublicModel(BaseModel):
    model_config = ConfigDict(extra='forbid')


class Links(PublicModel):
    github: HttpUrl
    linkedin: HttpUrl


class Profile(PublicModel):
    name: str
    headline: str
    location: str
    summary: str
    links: Links
    email: str
    whatsapp: HttpUrl


class SkillGroup(PublicModel):
    category: str
    technologies: list[str]


class Experience(PublicModel):
    id: str
    role: str
    start: str
    end: str | None
    context: str
    contributions: list[str]
    technologies: list[str]


class CaseStudy(PublicModel):
    id: str
    title: str
    context: str
    challenge: str
    solution: str
    outcome: str
    evidence: str
    technologies: list[str]


class Project(PublicModel):
    id: str
    title: str
    description: str
    technologies: list[str]
    repository: HttpUrl
    live_url: HttpUrl | None = None
    kind: str


class Education(PublicModel):
    title: str
    start_year: int
    end_year: int


class Portfolio(PublicModel):
    updated_at: str
    profile: Profile
    skills: list[SkillGroup]
    experiences: list[Experience]
    cases: list[CaseStudy]
    projects: list[Project]
    education: list[Education]
