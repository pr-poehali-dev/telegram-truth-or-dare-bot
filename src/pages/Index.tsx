import { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Card, CardContent } from '@/components/ui/card';
import Icon from '@/components/ui/icon';

const truthQuestions = [
  "Какую самую большую глупость ты совершил(-а) в жизни?",
  "Кого из присутствующих ты считаешь самым привлекательным?",
  "Какую тайну ты скрываешь от всех?",
  "О чём ты врал(-а) родителям?",
  "Какой твой самый стыдный момент в жизни?",
  "Что ты никогда не расскажешь своим родителям?",
  "Кто тебе нравится из этой компании?",
  "Какую оценку ты бы поставил(-а) своей внешности?",
  "Что самое безумное ты делал(-а) в нетрезвом состоянии?",
  "Кому из присутствующих ты завидуешь?",
  "Какое твоё самое большое сожаление?",
  "За что тебе больше всего стыдно?",
  "Кого бы ты поцеловал(-а) из присутствующих?",
  "Какой комплимент тебе было труднее всего принять?",
  "О чём ты думаешь перед сном?"
];

const dareActions = [
  "Станцуй танец без музыки в течение минуты",
  "Сделай комплимент каждому игроку",
  "Покажи последние 5 фотографий в телефоне",
  "Говори с акцентом до конца игры",
  "Отправь сообщение бывшему(-ей) 'Привет, как дела?'",
  "Сделай 20 приседаний",
  "Позвони родителям и скажи 'Я люблю вас'",
  "Покажи содержимое своей сумки или карманов",
  "Съешь что-нибудь, не используя руки",
  "Расскажи анекдот или смешную историю",
  "Сделай селфи с каждым игроком",
  "Покажи свой самый глупый танец",
  "Изобрази кого-то из присутствующих",
  "Спой песню, которую выберут другие",
  "Сделай планку 30 секунд"
];

export default function Index() {
  const [mode, setMode] = useState<'menu' | 'truth' | 'dare'>('menu');
  const [currentText, setCurrentText] = useState('');

  const handleTruth = () => {
    setMode('truth');
    const randomIndex = Math.floor(Math.random() * truthQuestions.length);
    setCurrentText(truthQuestions[randomIndex]);
  };

  const handleDare = () => {
    setMode('dare');
    const randomIndex = Math.floor(Math.random() * dareActions.length);
    setCurrentText(dareActions[randomIndex]);
  };

  const handleNext = () => {
    if (mode === 'truth') {
      const randomIndex = Math.floor(Math.random() * truthQuestions.length);
      setCurrentText(truthQuestions[randomIndex]);
    } else if (mode === 'dare') {
      const randomIndex = Math.floor(Math.random() * dareActions.length);
      setCurrentText(dareActions[randomIndex]);
    }
  };

  const handleBackToMenu = () => {
    setMode('menu');
    setCurrentText('');
  };

  return (
    <div className="min-h-screen flex items-center justify-center p-4">
      <div className="w-full max-w-md">
        {mode === 'menu' && (
          <div className="animate-fade-in">
            <h1 className="text-4xl font-bold text-center mb-2 text-foreground">
              Правда или Действие
            </h1>
            <p className="text-center text-muted-foreground mb-12 text-sm">
              Классическая игра для компании
            </p>

            <div className="space-y-4">
              <Button
                onClick={handleTruth}
                className="w-full h-32 text-2xl font-medium bg-primary hover:bg-primary/90 text-primary-foreground transition-all hover:scale-105"
              >
                <div className="flex flex-col items-center gap-3">
                  <Icon name="MessageCircle" size={40} />
                  <span>Правда</span>
                </div>
              </Button>

              <Button
                onClick={handleDare}
                className="w-full h-32 text-2xl font-medium bg-accent hover:bg-accent/90 text-accent-foreground transition-all hover:scale-105"
              >
                <div className="flex flex-col items-center gap-3">
                  <Icon name="Zap" size={40} />
                  <span>Действие</span>
                </div>
              </Button>
            </div>
          </div>
        )}

        {(mode === 'truth' || mode === 'dare') && (
          <div className="animate-scale-in">
            <div className="flex items-center justify-between mb-8">
              <Button
                onClick={handleBackToMenu}
                variant="ghost"
                size="sm"
                className="text-muted-foreground hover:text-foreground"
              >
                <Icon name="ArrowLeft" size={20} className="mr-2" />
                Назад
              </Button>
              <h2 className="text-xl font-semibold">
                {mode === 'truth' ? 'Правда' : 'Действие'}
              </h2>
              <div className="w-20" />
            </div>

            <Card className="mb-6 bg-card border-border">
              <CardContent className="p-8">
                <div className="flex justify-center mb-6">
                  <div className="w-16 h-16 rounded-full bg-primary/20 flex items-center justify-center">
                    <Icon
                      name={mode === 'truth' ? 'MessageCircle' : 'Zap'}
                      size={32}
                      className="text-primary"
                    />
                  </div>
                </div>
                <p className="text-center text-lg leading-relaxed">
                  {currentText}
                </p>
              </CardContent>
            </Card>

            <div className="space-y-3">
              <Button
                onClick={handleNext}
                className="w-full h-14 text-lg bg-primary hover:bg-primary/90 text-primary-foreground"
              >
                Следующий вопрос
              </Button>
              <Button
                onClick={handleBackToMenu}
                variant="outline"
                className="w-full h-14 text-lg border-border hover:bg-secondary"
              >
                Главное меню
              </Button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
