import CardComponent from "./CardComponent";
import QuickReplyButtons from "./QuickReplyButtons";
import CarouselComponent from "./CarouselComponent";
import LinkList from "./LinkList";

type StructuredResponseProps = {
  response: any;
  onUserAction: (value: string) => void;
};

export default function StructuredResponse({ response, onUserAction }: StructuredResponseProps) {
  if (!response || !response.content) return null;

  const { type } = response.content;

  switch (type) {
    case "card":
      return <CardComponent {...response.content} onUserAction={onUserAction} />;
    case "button":
      return <QuickReplyButtons {...response.content} onSelect={onUserAction} />;
    case "carousel":
      return <CarouselComponent {...response.content} onUserAction={onUserAction}/>;
    case "link":
      return <LinkList {...response.content} />;
    default:
      return (
        <pre className="text-xs text-gray-500">
          {JSON.stringify(response.content, null, 2)}
        </pre>
      );
  }
}
