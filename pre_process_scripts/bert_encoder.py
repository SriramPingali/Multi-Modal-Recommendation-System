
import nltk as __nltk
import numpy as __np
from transformers import AutoTokenizer as __AutoTokenizer
from transformers import AutoModel as __AutoModel


from tqdm import tqdm

# __tokenizer = AutoTokenizer.from_pretrained('allenai/scibert_scivocab_uncased')
# __model = AutoModel.from_pretrained('allenai/scibert_scivocab_uncased')

__tokenizer = __AutoTokenizer.from_pretrained('bert-base-uncased')
__model = __AutoModel.from_pretrained('bert-base-uncased')



def tokenize(list_of_paragraph):
	res= []
	for paragraph in list_of_paragraph:
		sentences= __nltk.sent_tokenize(paragraph)
		res.append(sentences)
	return res


def encode(list_of_paragraph, get_avg_of_each_paragraph= True, max_lines_to_take=None):
	res= list()
	list_of_sentences= tokenize(list_of_paragraph)
	for sentences in tqdm(list_of_sentences):
		res_for_this_para= list()
		for sentence in sentences:
			inputs = __tokenizer(sentence, return_tensors="pt")
			outputs= __model(**inputs)
			embedded=outputs['pooler_output']
			res_for_this_para.append(embedded[0].tolist())
		res_for_this_para= __np.array(res_for_this_para)
		if len(res_for_this_para) == 0: res_for_this_para= __np.zeros((1,768))

		if max_lines_to_take and len(res_for_this_para)>max_lines_to_take:
			res_for_this_para= res_for_this_para[:max_lines_to_take]

		# Make avg of all sentences of a paragraph
		avg_res= None
		if get_avg_of_each_paragraph:
			for item in res_for_this_para:
				if avg_res is None: avg_res= __np.zeros(len(item))
				avg_res= avg_res+item
			res_for_this_para= avg_res/len(res_for_this_para)
				

		res.append(res_for_this_para)
	return res










if __name__ == "__main__":

	__list_of_paragraph= ["hello there, how are you? I am doing alright... . hehe.",".", "", "I am doing alright. Thank you."]

	__res= encode(__list_of_paragraph)

	for __r in __res:
		print(__r.shape)
	



