# Supabase 설정 (최초 1회)

링크를 카톡으로 보내도 상대방이 열 수 있게 하려면 이 설정이 필요합니다.

## 1. SQL 실행

Supabase 대시보드 ▸ **SQL Editor** ▸ New query 에 아래를 통째로 붙여넣고 **Run**.

```sql
-- 프로젝트 (이름 · 분류 · 공유상태)
create table if not exists public.spa_projects (
  id           text primary key,
  name         text not null,
  categories   jsonb not null default '[]'::jsonb,
  share_active boolean not null default false,
  updated_at   timestamptz not null default now()
);

-- 체크포인트 · 의견 (프로젝트당 1행, 배열 통째로)
create table if not exists public.spa_pins (
  project_id text primary key references public.spa_projects(id) on delete cascade,
  pins       jsonb not null default '[]'::jsonb,
  updated_at timestamptz not null default now()
);

-- RLS: anon 키로 읽기/쓰기 허용 (공유 비밀번호 없는 단순 공유)
alter table public.spa_projects enable row level security;
alter table public.spa_pins     enable row level security;

drop policy if exists spa_projects_all on public.spa_projects;
create policy spa_projects_all on public.spa_projects
  for all to anon, authenticated using (true) with check (true);

drop policy if exists spa_pins_all on public.spa_pins;
create policy spa_pins_all on public.spa_pins
  for all to anon, authenticated using (true) with check (true);

-- 사진 저장용 버킷 (공개)
insert into storage.buckets (id, name, public)
values ('spa-photos', 'spa-photos', true)
on conflict (id) do update set public = true;

drop policy if exists spa_photos_read   on storage.objects;
drop policy if exists spa_photos_write  on storage.objects;
drop policy if exists spa_photos_delete on storage.objects;

create policy spa_photos_read on storage.objects
  for select to anon, authenticated using (bucket_id = 'spa-photos');

create policy spa_photos_write on storage.objects
  for insert to anon, authenticated with check (bucket_id = 'spa-photos');

create policy spa_photos_delete on storage.objects
  for delete to anon, authenticated using (bucket_id = 'spa-photos');
```

## 2. 확인

`config.js` 에 `SUPABASE_URL` / `SUPABASE_ANON_KEY` 가 채워져 있으면 끝입니다.
앱을 열면 우측 하단에 **☁ 클라우드** 표시가 뜹니다.

- 기존에 이 PC에서 만든 프로젝트·체크포인트·사진은 **처음 한 번 자동으로 업로드**됩니다.
- 이후 `🔗 링크` 로 만든 주소는 카톡으로 보내도 상대방 폰에서 열립니다.

## 주의

anon 키만 쓰는 단순 공유 구조입니다. 링크를 아는 사람은 누구나 열람할 수 있고,
`🔗 링크` 팝업에서 **공유 끄기**를 하면 즉시 차단됩니다.
