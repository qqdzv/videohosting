import React, { useState } from 'react';
import { useGetCommentsQuery, useCreateCommentMutation, useEditCommentMutation, useDeleteCommentMutation } from '../../store/api/comment.api';
import { useGetProfileQuery } from '../../store/api/auth.api';
import { CommentView } from '../../api/types';
import styles from './Comments.module.scss';

interface CommentsProps {
  videoId: number;
}

interface EditingComment {
  id: number;
  text: string;
}

export const Comments: React.FC<CommentsProps> = ({ videoId }) => {
  const [commentText, setCommentText] = useState('');
  const [editingComment, setEditingComment] = useState<EditingComment | null>(null);
  const [activeDropdown, setActiveDropdown] = useState<number | null>(null);
  const { data: comments = [], isLoading } = useGetCommentsQuery(videoId);
  const [createComment] = useCreateCommentMutation();
  const [editComment] = useEditCommentMutation();
  const [deleteComment] = useDeleteCommentMutation();
  const { data: profile } = useGetProfileQuery();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!commentText.trim()) return;

    try {
      await createComment({
        videoId,
        data: { text: commentText }
      });
      setCommentText('');
    } catch (error) {
      console.error('Не удалось создать комментарий:', error);
    }
  };

  const handleEdit = (comment: CommentView) => {
    if (comment.id === undefined || comment.text === undefined) return;
    setEditingComment({ id: comment.id, text: comment.text });
    setActiveDropdown(null);
  };

  const handleDelete = async (commentId: number) => {
    try {
      await deleteComment(commentId);
      setActiveDropdown(null);
    } catch (error) {
      console.error('Не удалось удалить комментарий:', error);
    }
  };

  const handleCancelEdit = () => {
    setEditingComment(null);
  };

  const handleSaveEdit = async (commentId: number) => {
    if (!editingComment || !editingComment.text.trim()) return;

    try {
      await editComment({
        commentId,
        data: { text: editingComment.text }
      });
      setEditingComment(null);
    } catch (error) {
      console.error('Не удалось отредактировать комментарий:', error);
    }
  };

  const handleEditInputChange = (text: string) => {
    if (editingComment) {
      setEditingComment({
        id: editingComment.id,
        text
      });
    }
  };

  const toggleDropdown = (commentId: number | undefined) => {
    if (!commentId) return;
    setActiveDropdown(activeDropdown === commentId ? null : commentId);
  };

  // Close dropdown when clicking outside
  const handleClickOutside = (e: MouseEvent) => {
    const target = e.target as HTMLElement;
    if (!target.closest(`.${styles.actionsDropdown}`) && !target.closest(`.${styles.actionButton}`)) {
      setActiveDropdown(null);
    }
  };

  React.useEffect(() => {
    document.addEventListener('click', handleClickOutside);
    return () => {
      document.removeEventListener('click', handleClickOutside);
    };
  }, []);

  if (isLoading) {
    return <div>Загрузка комментариев...</div>;
  }

  return (
    <div className={styles.container}>
      <h2 className={styles.title}>{comments.length} комментариев</h2>

      <form className={styles.commentForm} onSubmit={handleSubmit}>
        <img
          src={profile?.avatar || `https://ui-avatars.com/api/?name=${profile?.username}`}
          alt="Your avatar"
          className={styles.avatar}
        />
        <div className={styles.inputWrapper}>
          <input
            type="text"
            value={commentText}
            onChange={(e) => setCommentText(e.target.value)}
            placeholder="Добавить комментарий..."
            className={styles.input}
          />
          <button 
            type="submit" 
            className={styles.submitButton}
            disabled={!commentText.trim()}
          >
            Отправить
          </button>
        </div>
      </form>

      <div className={styles.commentsList}>
        {comments.map((comment) => (
          <div key={comment.id} className={styles.comment}>
            <img
              src={comment.avatar || `https://ui-avatars.com/api/?name=${comment.username}`}
              alt={`${comment.first_name} ${comment.last_name}`}
              className={styles.avatar}
            />
            <div className={styles.commentContent}>
              <div className={styles.commentHeader}>
                <span className={styles.authorName}>
                  {comment.first_name} {comment.last_name}
                </span>
                <span className={styles.username}>@{comment.username}</span>
                <span className={styles.date}>
                  {new Date(comment.created_at || '').toLocaleDateString()}
                </span>
                {profile?.username === comment.username && comment.id !== undefined && (
                  <div className={styles.actions}>
                    <button
                      className={styles.actionButton}
                      onClick={() => toggleDropdown(comment.id)}
                    >
                      ⋮
                    </button>
                    {activeDropdown === comment.id && (
                      <div className={styles.actionsDropdown}>
                        <button onClick={() => handleEdit(comment)}>
                          Редактировать
                        </button>
                        <button onClick={() => comment.id && handleDelete(comment.id)}>
                          Удалить
                        </button>
                      </div>
                    )}
                  </div>
                )}
              </div>
              {editingComment?.id === comment.id ? (
                <div className={styles.editForm}>
                  <input
                    type="text"
                    value={editingComment?.text}
                    onChange={(e) => handleEditInputChange(e.target.value)}
                    className={styles.editInput}
                  />
                  <div className={styles.editButtons}>
                    <button
                      onClick={() => comment.id && handleSaveEdit(comment.id)}
                      disabled={!editingComment?.text.trim()}
                      className={styles.saveButton}
                    >
                      Сохранить
                    </button>
                    <button
                      onClick={handleCancelEdit}
                      className={styles.cancelButton}
                    >
                      Отмена
                    </button>
                  </div>
                </div>
              ) : (
                <p className={styles.commentText}>{comment.text}</p>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}; 