#pragma once
#include <string>
#include <functional>
#include "mpnode.h"


using namespace std;

// �������(��������һ����������)

class MPList
{
public:
	// ���캯��
	MPList();
	// ���캯��
	// MPList(string);
	// ��������
	~MPList();
	// ��ȡ����ʽ�����ĳ���
	size_t GetLength() const;
	// ��ȡ����ʽ���������
	size_t GetDepth() const;
	// ��ȡ����ʽ������Ƿ�Ϊ�ձ�
	bool IsEmpty() const;
	// ��ȡ����ʽ�����ı�ͷ�ڵ㣬�ձ�ͷ����nullptr
	MPNode* GetHead() const;
	// ��ȡ����ʽ�����ı�β�ڵ㣬�ձ�β����nullptr
	MPNode* GetTail() const;
	// ��ȡ��Ԫ����
	size_t GetVarNums() const;
	// ��ȡ��ǰ����ʽ�����Ķ�����Ԫ��
	char GetVarName() const;
	// ͷ��ڵ㣨��ָͬ����Զ��ϲ���
	bool InsertFirst(MPNode);
	// β��ڵ㣨��ָͬ����Զ��ϲ���
	bool InsertEnd(MPNode);
	// ͷɾ�ڵ�
	bool DeleteFirst();
	// �����������ʽ�����
	friend MPList* operator *(const MPList&, const MPList&);
	// ����ʽ������ϵ�����
	friend MPList* operator *(const MPList&, float);
	friend MPList* operator *(float, const MPList&);
	// �����͹�������
	friend MPList* operator +(const MPList&, const MPList&);
	// ������ϵ�����
	friend MPList* operator +(const MPList&, float);
	friend MPList* operator +(float, const MPList&);
	// ��ȡ�ַ�����ʾ
	string ToString();
	// ���ַ�����ʾ��ʼ������ʽ�����
	void FromString(string);
	// ���ݹ����ָ�������������ӽڵ㣨�������޸Ľڵ㣩
	void ForEachC(function<void(const MPNode&)>) const;
	// ���ݹ����ָ�������������ӽڵ㣨�����޸Ľڵ㣩
	void ForEach(function<void(MPNode&)>);
	// �������������
	friend ostream& operator <<(ostream&, MPList&);
	friend istream& operator >>(istream&, MPList&);

private:
	MPNode* head_ptr;
	MPNode* tail_ptr;
	size_t length;
	char var_name;
};

