import { copyFile } from "fs/promises";
import { fileURLToPath } from "url";
import path from "path";

// __dirname аналог
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// пути
const sourcePath = path.resolve(__dirname, "../backend/.env"); // измените при необходимости
const destinationPath = path.resolve(__dirname, ".env");

try {
  await copyFile(sourcePath, destinationPath);
  console.log(`✅ .env успешно скопирован из: ${sourcePath}`);
} catch (err) {
  console.error(`❌ Ошибка при копировании .env: ${err.message}`);
  process.exit(1);
}
