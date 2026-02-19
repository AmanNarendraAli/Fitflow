# FitFlow (Multi‑Tenant Gym SaaS) — Django Workplan

Goal: Build a **multi‑tenant** gym / fitness studio SaaS that is clearly more complex than CRUD inventory, but still manageable while you’re learning Django.

**Recommended multi‑tenancy (starter-friendly):** Shared DB + shared tables + **row‑level isolation** via a `gym` (tenant) foreign key on every tenant‑owned model.

---

## 0) Repo + tooling setup (Day 0)

### Tasks
- [x] Create repo + virtualenv
- [x] Install core deps:
- [x] Create project: `fitflow/` + app(s): `accounts`, `core`, `classes`, `billing` (you can start with fewer)

### Deliverables
- Project runs locally
- `.env` loaded for secrets
- Basic homepage renders

### Acceptance checks
- `python manage.py runserver` works
- `python manage.py check` passes

---

## 1) Multi-tenant foundation + auth + roles (Phase 1)

### Design decisions (keep simple)
- A user belongs to **exactly one** gym for now.
- Tenant choice: **Gym join code** (easiest). Later you can add subdomains.

### Models
- `Gym`: `name`, `code` (unique), `timezone`, `created_at`
- Custom `User` (recommended early):
  - `gym = FK(Gym)`
  - `role = choices: OWNER, STAFF, TRAINER, MEMBER`
  - email as login (optional)

### Tasks
- [x] Create custom user model (do this early before migrations get heavy)
- [x] Sign up flow:
  - Create gym (owner creates gym + first owner account)
  - Join gym via code (members/staff join existing gym)
- [x] Role-based access helpers:
  - Decorators / mixins like `@role_required("OWNER")`
- [x] Tenant safety:
  - **Every query must filter by `request.user.gym`**
  - Add tenant-aware base queryset helpers (e.g., `GymQuerySetMixin`)

### Deliverables
- Users can:
  - Create a gym + become OWNER
  - Join a gym via code + become MEMBER (or STAFF/TRAINER if invited)
- Basic nav + login/logout

### Acceptance checks
- User A cannot access User B’s gym data (manual test)
- Trying to visit other gym’s URLs returns 404 or 403

---

## 2) Core “gym objects” + admin panel polish (Phase 2A)

### Models
- `Room` (optional): `gym`, `name`, `capacity`
- `TrainerProfile`: `gym`, `user`, `bio`, `specialties`
- `MemberProfile`: `gym`, `user`, `phone`, `emergency_contact`

### Tasks
- [x] CRUD for Rooms (OWNER only)
- [ ] CRUD for trainer/member profiles (OWNER/STAFF)
- [ ] Admin dashboard scaffold:
  - “Today’s sessions”
  - “Upcoming sessions”
  - “Recent bookings”
  - “Active members count”

### Deliverables
- OWNER can manage rooms + see dashboard stats
- STAFF can view members + trainers (but limited edits)

### Acceptance checks
- Permissions are enforced (role-based)
- All objects are gym-scoped (tenant-safe)

---

## 3) Classes + scheduling (Phase 2B)

This is the biggest “non‑CRUD” upgrade: time logic + constraints.

### Models
- `ClassType`: `gym`, `name`, `duration_minutes`, `default_capacity`
- `ClassSession`: `gym`, `class_type`, `trainer`, `room` (optional), `starts_at`, `ends_at`, `capacity`, `status`
  - (You can derive `ends_at` from duration if you want.)

### Tasks
- Create session creation UI (OWNER/STAFF)
- Session calendar/list views:
  - “This week”
  - “Today”
  - Filter by trainer/class type
- Validation:
  - `ends_at > starts_at`
  - capacity > 0
  - (optional) avoid room overlap

### Deliverables
- Gym staff can create scheduled sessions
- Members can view schedule

### Acceptance checks
- Session list only shows `request.user.gym` sessions
- Form validation blocks invalid times/capacities

---

## 4) Booking system (Phase 3)

### Model
- `Booking`: `gym`, `session`, `member`, `status` (BOOKED/CANCELLED/NO_SHOW/CHECKED_IN), `created_at`

### Tasks
- Member booking flow:
  - Book a session
  - Cancel booking (with policy: e.g., cancel allowed until X hours before start)
- Capacity enforcement:
  - Don’t allow bookings above capacity
  - Use DB-level safety:
    - `UniqueConstraint(gym, session, member)` to prevent duplicates
    - Transaction when booking to prevent race conditions
- Conflict detection:
  - Don’t allow member to book overlapping sessions

### Deliverables
- Booking + cancellation fully functional
- Session page shows roster (TRAINER/STAFF)

### Acceptance checks
- Cannot exceed capacity
- Member cannot book same session twice
- Overlapping bookings are rejected

---

## 5) Check-in + attendance (Phase 4A)

### Tasks
- Staff check-in screen:
  - Search member
  - Mark booking as CHECKED_IN
  - Walk-in flow (optional): create booking + check-in instantly if capacity allows
- Trainer view:
  - “My sessions today”
  - Roster list with check-in status

### Deliverables
- End-to-end “front desk” workflow
- Trainer roster view works

### Acceptance checks
- STAFF can check-in; MEMBER cannot
- Attendance reflected in dashboards

---

## 6) Membership plans + credits (no payments) (Phase 4B)

Avoid Stripe initially—still show real product logic.

### Models
- `MembershipPlan`: `gym`, `name`, `plan_type` (UNLIMITED / PACK), `monthly_price` (optional), `credits` (for PACK)
- `Subscription`: `gym`, `member`, `plan`, `status`, `credits_remaining`, `start_date`, `end_date`

### Rules
- UNLIMITED: no credit deduction
- PACK: booking deducts 1 credit (or deduct on check-in—pick one and document it)
- No credits => block booking

### Tasks
- Plan management (OWNER)
- Subscription assignment (STAFF/OWNER)
- Credit deduction logic
- Member profile shows plan + credits

### Deliverables
- Bookings respect plan rules
- Credits update correctly

### Acceptance checks
- PACK members cannot book with 0 credits
- UNLIMITED members can always book (capacity permitting)

---

## 7) Role dashboards + “SaaS feel” (Phase 5)

### Dashboards
- OWNER:
  - Active members, sessions this week, utilization, no-shows
- STAFF:
  - Today schedule + check-in queue
- TRAINER:
  - My sessions + rosters
- MEMBER:
  - My bookings + plan + credits

### Tasks
- Build each dashboard view + template
- Add basic analytics (counts, rates)
- Add pagination + search where needed

### Deliverables
- App feels like a real product with role-specific UX

### Acceptance checks
- Each role sees different dashboard and cannot access others’ admin pages

---

## 8) Hardening: tenant safety, permissions, testing (Phase 6)

### Tasks
- Add tenant-safe query helpers:
  - Base manager that requires gym scoping
- Add unit tests:
  - tenant isolation test (cannot read others)
  - permission tests per role
  - booking capacity test
- Add basic security:
  - CSRF, secure cookies in prod, password reset

### Deliverables
- A test suite that prevents tenant leaks
- Confidence to refactor safely

### Acceptance checks
- `pytest` / `manage.py test` passes
- “Cross-tenant access” tests fail if you accidentally remove gym filter

---

## 9) Deployment (Phase 7)

### Tasks
- Choose one:
  - Render / Fly.io / Railway / DigitalOcean
- Use Postgres in prod
- Configure static files (Whitenoise recommended for simplicity)
- Set env vars + allowed hosts

### Deliverables
- Live hosted app with at least 2 gyms working

### Acceptance checks
- Can create Gym A + Gym B
- Confirm tenant isolation on production

---

# Suggested scope to stop at (clean portfolio version)

If you want a strong project without overbuilding:

✅ Multi-tenant + roles  
✅ Scheduling + booking + capacity + overlap prevention  
✅ Check-in workflow  
✅ Membership plans + credits (no Stripe)  
✅ Dashboards per role  

---

# Architecture notes (what to say in interviews)

- “Multi-tenant row-level isolation via tenant FK on all models”
- “Role-based access with decorators/mixins”
- “Transactional booking to enforce capacity + uniqueness constraints”
- “Tenant-leak regression tests”

---

# Optional stretch features (pick at most 1–2)

- Subdomain tenancy (`{gym}.fitflow.com`)
- Waitlist when class is full
- Announcements + read receipts
- Staff invites via email token
- Export attendance CSV
