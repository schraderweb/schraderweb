create table if not exists public.form_submissions (
  id bigint generated always as identity primary key,
  created_at timestamptz not null default now(),
  name text not null,
  phone text not null,
  email text,
  message text
);
