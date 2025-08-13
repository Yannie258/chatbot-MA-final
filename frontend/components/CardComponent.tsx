type CardContent = {
  title: string;
  description: string;
  image_url?: string | null;
  action_url?: string;
  action_label?: string;
};

export default function CardComponent({ title, description, image_url, action_url,
  action_label = "Learn more" }: CardContent) {
  return (
    <div className="border p-4 rounded shadow bg-white max-w-xs">
      {image_url && (
        <img
          src={image_url}
          alt={title}
          className="w-full h-32 object-cover rounded mb-2"
        />
      )}
      <h3 className="text-lg font-semibold mb-1">{title}</h3>
      <p className="text-sm text-gray-700">{description}</p>
      {action_url && (
        <button
          onClick={() => window.open(action_url, "_blank")}
          className="bg-blue-600 text-white px-3 py-1 rounded hover:bg-blue-500 text-sm"
        >
          {action_label}
        </button>
      )}
    </div>
  );
}
