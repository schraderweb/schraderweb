create table if not exists public.form_submissions (
  id bigint generated always as identity primary key,
  created_at timestamptz not null default now(),
  first_name text not null,
  last_name text not null,
  phone text not null,
  email text,
  company text,
  service text,
  consent boolean default false,
  message text,
  budget_range text
);
