export const formatViewsCount = (views: number): string => {
    if (views >= 1000000) {
        return `${(views / 1000000).toFixed(1)}M`;
    }
    if (views >= 1000) {
        return `${(views / 1000).toFixed(1)}K`;
    }
    return views.toString();
};

export const formatRelativeDate = (dateString: string): string => {
    const date = new Date(dateString);
    const now = new Date();
    const diffInSeconds = Math.floor((now.getTime() - date.getTime()) / 1000);
    const diffInMinutes = Math.floor(diffInSeconds / 60);
    const diffInHours = Math.floor(diffInMinutes / 60);
    const diffInDays = Math.floor(diffInHours / 24);
    const diffInMonths = Math.floor(diffInDays / 30);
    const diffInYears = Math.floor(diffInDays / 365);

    if (diffInYears > 0) {
        return `${diffInYears} ${diffInYears === 1 ? 'год' : diffInYears < 5 ? 'года' : 'лет'} назад`;
    }
    if (diffInMonths > 0) {
        return `${diffInMonths} ${diffInMonths === 1 ? 'месяц' : diffInMonths < 5 ? 'месяца' : 'месяцев'} назад`;
    }
    if (diffInDays > 6) {
        const weeks = Math.floor(diffInDays / 7);
        return `${weeks} ${weeks === 1 ? 'неделю' : weeks < 5 ? 'недели' : 'недель'} назад`;
    }
    if (diffInDays > 0) {
        return `${diffInDays} ${diffInDays === 1 ? 'день' : diffInDays < 5 ? 'дня' : 'дней'} назад`;
    }
    if (diffInHours > 0) {
        return `${diffInHours} ${diffInHours === 1 ? 'час' : diffInHours < 5 ? 'часа' : 'часов'} назад`;
    }
    if (diffInMinutes > 0) {
        return `${diffInMinutes} ${diffInMinutes === 1 ? 'минуту' : diffInMinutes < 5 ? 'минуты' : 'минут'} назад`;
    }
    return 'только что';
}; 