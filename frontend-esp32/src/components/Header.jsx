const now = new Date()

export default function Header(){
    return (
      <header className="bg-gradient-to-r from-blue-500 to-indigo-600 text-white py-6 shadow-lg">
      <div className="container mx-auto flex justify-between items-center px-6">
        <h1 className="text-3xl font-extrabold tracking-wide">ESP32</h1>
        <nav>
          <ul className="flex space-x-6 text-lg">
            <li><a href="#" className="hover:underline">{now.toLocaleTimeString()}</a></li>
            <li><a href="#" className="hover:underline">О проекте</a></li>
            <li><a href="#" className="hover:underline">Контакты</a></li>
          </ul>
        </nav>
      </div>
    </header>
  );
}