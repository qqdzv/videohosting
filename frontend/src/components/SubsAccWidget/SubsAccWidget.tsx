import { FC } from 'react';
import cls from './SubsAccWidget.module.scss';
import { Button } from '@/ui/Button/Button';

interface SubsAccWidgetProps {
	preview?: string;
	author: string;
	name: string;
	lastVideous?: string[];
}
export const SubsAccWidget: FC<SubsAccWidgetProps> = () => {
	return (
		<article className={cls.subsAccWidget}>
			<div className={cls.channelInfo}>
				<img src="/icons/account.png" alt="account" className={cls.avatar} />
				<section className={cls.info}>
					<span>Channel Name</span>
					<p>1066 subsribers</p>
				</section>
			</div>
			<div className={cls.lastVideous}>
				<h2 className={cls.title}>Последние видео</h2>
				<div className={cls.videos}>
					{[...Array(3)].map((_, index) => (
						<div className={cls.video} key={index}>
							<div className={cls.preview} />
							<div className={cls.videoInfo}>
								<span className={cls.name}>Как выучить фронтенд за сутки? | Реальнный гайд</span>
								<p className={cls.views}>12.124 views</p>
							</div>
						</div>
					))}
				</div>
			</div>
			<Button text="Подписаться" size="s" onClick={() => {}} primary style={{alignSelf: "center"}}/>
		</article>
	);
};
