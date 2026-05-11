-- 0001_birth_profiles.sql
-- The ancestral record table, sealed by Row-Level Security.
-- Apply via Supabase SQL editor or `supabase db push`.

create extension if not exists "pgcrypto";

create table if not exists public.birth_profiles (
    id              uuid primary key default gen_random_uuid(),
    user_id         uuid not null references auth.users(id) on delete cascade,
    name            text not null check (char_length(name) between 1 and 255),
    birth_datetime  timestamptz not null,
    latitude        double precision not null check (latitude between -90 and 90),
    longitude       double precision not null check (longitude between -180 and 180),
    created_at      timestamptz not null default now()
);

create index if not exists birth_profiles_user_id_idx
    on public.birth_profiles (user_id);

-- The Spirit Gate: enforce RLS so each seeker sees only their own records.
alter table public.birth_profiles enable row level security;

drop policy if exists "seekers read their own profiles" on public.birth_profiles;
create policy "seekers read their own profiles"
    on public.birth_profiles
    for select
    using (auth.uid() = user_id);

drop policy if exists "seekers insert their own profiles" on public.birth_profiles;
create policy "seekers insert their own profiles"
    on public.birth_profiles
    for insert
    with check (auth.uid() = user_id);

drop policy if exists "seekers update their own profiles" on public.birth_profiles;
create policy "seekers update their own profiles"
    on public.birth_profiles
    for update
    using (auth.uid() = user_id)
    with check (auth.uid() = user_id);

drop policy if exists "seekers delete their own profiles" on public.birth_profiles;
create policy "seekers delete their own profiles"
    on public.birth_profiles
    for delete
    using (auth.uid() = user_id);
