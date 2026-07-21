-- 1. Agregar columna is_approved a la tabla profiles si no existe (por defecto false)
ALTER TABLE public.profiles ADD COLUMN IF NOT EXISTS is_approved BOOLEAN DEFAULT false;

-- 2. Auto-aprobar a los administradores conocidos
UPDATE public.profiles SET is_approved = true WHERE email IN ('canelakinta@gmail.com', 'navpercris@gmail.com');

-- 3. Actualizar la función trigger para que los nuevos usuarios se registren como desaprobados (false)
CREATE OR REPLACE FUNCTION public.handle_new_user()
RETURNS trigger AS $$
BEGIN
  INSERT INTO public.profiles (id, username, email, avatar_url, is_approved)
  VALUES (
    NEW.id,
    COALESCE(NEW.raw_user_meta_data->>'username', split_part(NEW.email, '@', 1)),
    NEW.email,
    'https://api.dicebear.com/7.x/pixel-art/svg?seed=' || COALESCE(NEW.raw_user_meta_data->>'username', split_part(NEW.email, '@', 1)),
    false -- Nuevos usuarios quedan desaprobados por defecto
  );
  RETURN NEW;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;
